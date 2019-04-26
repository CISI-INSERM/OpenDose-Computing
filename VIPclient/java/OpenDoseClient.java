
import org.carmin.client.*;
import org.carmin.client.api.DefaultApi;
import org.carmin.client.model.Execution;
//import org.carmin.client.model.Path;
import org.carmin.client.model.Pipeline;

import java.io.*;
//import java.io.FileNotFoundException;
//import java.nio.file.Paths;
import java.text.SimpleDateFormat;
import java.util.*;
import java.text.DateFormat;
import java.util.regex.Matcher;
import java.util.regex.Pattern;


/**
 * Created by gmathieu
 * Based on a squeleton file created by abonnet
 */

public class OpenDoseClient {

    private final DefaultApi vipApi;


    public static void main(String[] args) throws IOException, ApiException {

        // path to the local configuration file used to set workflow execution parameters
        String configDir = "/home/gate/opendose/config/";

        // call constructor to instantiate now client object
        OpenDoseClient client = new OpenDoseClient(configDir);

        // Execute workflow
        client.executeWorkflow(configDir);

        // get results
        //client.getOutputs();
    }


    // Constructor
    private OpenDoseClient (String configDir) throws FileNotFoundException {
        // get API URL from the local config file where it is set
        Scanner sApiUrl = new Scanner(new File(configDir+"/apiURL.txt"));
        String apiURL = sApiUrl.next();
        sApiUrl.close();

        // get user API key from the local config file where it is set
        Scanner sApiKey = new Scanner(new File(configDir+"/apiKey.txt"));
        String APIKey = sApiKey.next();
        sApiKey.close();

        // ******** INIT API CLIENT ***********
        ApiClient vipApiClient = new ApiClient();
        vipApiClient.setApiKey(APIKey);// Key GM
        vipApiClient.setBasePath(apiURL);
        vipApi = new DefaultApi(vipApiClient);
    }


    private void executeWorkflow (String configDir) throws IOException
    {
        // ********** SET VARIABLES AND PARSE CONFIG FILE TO INIT INPUTS ***********
        // set execution date
        DateFormat daytime = new SimpleDateFormat("yyyy-MM-dd_HHmmss");
        Date today = Calendar.getInstance().getTime();
        String reportDate = daytime.format(today);
        // open config file
        String configFileName = configDir+"/exec_config.txt";
        Scanner sconfig;
        sconfig = new Scanner(new File(configFileName));
        // start parsing config file
        sconfig.next();
        // application to be used (GateLab or GateCLforOpenDose
        String usedApplication = sconfig.next();
        sconfig.nextLine();
        sconfig.next();
        // CPU estimation parameter (only used by GateLab)
        String cpuParam = sconfig.next();
        sconfig.nextLine();
        sconfig.next();
        // path to the local file containing the list of source organs to be used as input
        String organsListPathName = sconfig.next();
        sconfig.nextLine();
        sconfig.next();
        // path to the local file containing the list of energies to be used as input
        String energiesListPathName = sconfig.next();
        sconfig.nextLine();
        sconfig.next();
        // particle to simulate
        String particle = sconfig.next();
        sconfig.nextLine();
        sconfig.next();
        // Number of primaries for the simulations
        String numberOfPrimaries = sconfig.next();
        sconfig.nextLine();
        sconfig.next();
        // LFN of the input zip archive
        String gateInputLFN = sconfig.next();
        sconfig.nextLine();
        sconfig.next();
        // Path to the Gate Release to be used
        String gateReleasePath = sconfig.next();
        sconfig.nextLine();
        sconfig.next();
        // Name of the MAC file to be used
        String macFileName = sconfig.next();
        sconfig.nextLine();
        sconfig.next();
        // local directory in which to write log file
        String reportDir = sconfig.next();
        sconfig.nextLine();
        sconfig.next();
        // local file linking params with workflow id
        String reportFile = sconfig.next();
        sconfig.nextLine();
        sconfig.next();
        // output directory on VIP (only used for GateCLforOpenDose)
        String outputDir = sconfig.next();
        sconfig.close();
        // path to the local log file to which we will write execution report
        String reportFilePathName = reportDir + "exec_log_"+reportDate+".txt";

        // Get model from macfilename
        String modelName = "AM";
        Pattern regexp = Pattern.compile("AF");
        Matcher regexm = regexp.matcher(particle);
        while(regexm.find()) {
            modelName = "AF";
        }


        // build list of source organs from input data
        ArrayList<String> organsList = new ArrayList<>();
        Scanner s1 = new Scanner(new File(configDir+"/"+organsListPathName));
        while (s1.hasNextLine()){
            organsList.add(s1.nextLine());
        }
        s1.close();

        // build list of energy levels from input data
        ArrayList<String> energiesList = new ArrayList<>();
        Scanner s2 = new Scanner(new File(configDir+"/"+energiesListPathName));
        while (s2.hasNextLine()){
            energiesList.add(s2.nextLine());
        }
        s2.close();

        // ********** CREATE LOCAL LOG FILE ***********
        File clientExecutionLog = new File(reportFilePathName);
        try{
            clientExecutionLog.createNewFile();
        } catch (IOException e) {
            System.out.println("unable to create local log file");
            e.printStackTrace();
        }
        String reportFileCompletePath = reportDir + reportFile;
        FileWriter clientReportFileWriter = new FileWriter(reportFileCompletePath, true);

        // ********** INITIALIZE LOCAL LOG FILE ***********
        FileWriter writer = new FileWriter(clientExecutionLog);
        writer.write("OPENDOSE EXECUTION REPORT - " + reportDate + "\n\n");
        writer.write("used application: " + usedApplication + "\n\n");
        writer.write("used MAC file: " + macFileName + "\n");
        writer.write("number of primaries: " + numberOfPrimaries + "\n");
        writer.write("used input file for gate: " + gateInputLFN + "\n");
        writer.write("used gate release: " + gateReleasePath + "\n");
        writer.write("\n---BEGIN---\n");

        // ********** SET PIPELINE ***********
        String executionName;
        String jobIdentifier ="";
        Date nowDate;
        String nowFormatted;
        Execution execution = new Execution();
        Map<String, Object> inputValues = new HashMap<>();

        switch(usedApplication){

            // *********************** GATELAB ***********************************
            case "GateLab": // GateLab inputs and execution setup
                execution.setPipelineIdentifier("GateLab/0.7.2");
                inputValues.put("CPUestimation", cpuParam);
                inputValues.put("ParallelizationType", "stat");
                inputValues.put("GateRelease", gateReleasePath);
                inputValues.put("NumberOfParticles", numberOfPrimaries);
                inputValues.put("GateInput", gateInputLFN);
                // loop over all organs found in input matrix
                for (String organ_alias : organsList) {
                    // loop over all energies found in input matrix
                    for (String energy_alias : energiesList) {
                        String seed = this.computeSeed(macFileName, organ_alias, particle, energy_alias);
                        String alias_string;
                        alias_string = "-a [Source_ID," + organ_alias + "][particle," + particle + "][energy," + energy_alias + "][nb," + numberOfPrimaries + "][seed," + seed + "]";
                        inputValues.put("phaseSpace", alias_string);
                        executionName = "OpenDose_GateLab" + "_" + organ_alias + "_" + particle + "_" + energy_alias + "_" + numberOfPrimaries;

                        // setup and launch execution
                        execution.setInputValues(inputValues);
                        execution.setName(executionName);
                        try {
                            execution = vipApi.initExecution(execution);
                        } catch (ApiException e) {
                            e.printStackTrace();
                        }
                        jobIdentifier = execution.getIdentifier();
                        System.out.println(jobIdentifier);
                        nowDate = Calendar.getInstance().getTime();
                        nowFormatted = daytime.format(nowDate);
                        writer.write(nowFormatted + " : " + executionName + " - " + jobIdentifier + "\n");
                        clientReportFileWriter.write (modelName + "," + organ_alias + "," + particle + "," + energy_alias + "," + numberOfPrimaries + "," + seed + "," + cpuParam + "," + jobIdentifier + "\n");
                        System.out.println(executionName);
                    }
                }
                break;
            // *********************** GATECLFOROPENDOSE ***********************************
            case "GateCLforOpenDose": // GateCLforOpenDose inputs and execution setup
                execution.setPipelineIdentifier("GateCLforOpenDose/v0.2.0");
                inputValues.put("indata", gateInputLFN);
                inputValues.put("gatereleasepath", gateReleasePath);
                inputValues.put("nbprimaries", numberOfPrimaries);
                inputValues.put("macfile", macFileName);
                inputValues.put("results-directory", outputDir);
                inputValues.put("organid", organsList);
                inputValues.put("particletype", particle);
                inputValues.put("energy", energiesList);
                executionName = "OpenDose_GateCLforOpenDose" + "_" + particle + "_" + numberOfPrimaries;
                // setup and launch execution
                execution.setInputValues(inputValues);
                execution.setName(executionName);
                try {
                    execution = vipApi.initExecution(execution);
                } catch (ApiException e) {
                    e.printStackTrace();
                }
                jobIdentifier = execution.getIdentifier();
                System.out.println(jobIdentifier);
                nowDate= Calendar.getInstance().getTime();
                nowFormatted  = daytime.format(nowDate);
                writer.write(nowFormatted + " : " + executionName + " - " + jobIdentifier + "\n");
                System.out.println(executionName);
                break;
            // ********* ERROR HANDLING *************
            default:
                System.out.println("Unknown application. Can't execute anything.");
                break;
        }
        writer.write("---END---");
        writer.close();
        clientReportFileWriter.close();
    }

    private String computeSeed (String model, String source, String particle, String energy)
    {
        // define numerical value corresponding to chosen model
        // if model is AF, m=0. If model is AM, m=500
        int m = 0;
        Pattern regexp = Pattern.compile("AM");
        Matcher regexm = regexp.matcher(model);
        while(regexm.find()) {
            m = 500;
        }

        // define numerical value corresponding to chosen particle
        int p = 0;
        regexp = Pattern.compile("gamma");
        regexm = regexp.matcher(particle);
        while(regexm.find()) {
            p = 200;
        }

        // get numerical value from source organ ID
        int s = Integer.parseInt(source);

        // get numerical value from energy
        double e = Double.parseDouble(energy);

        // calculate seed
        // get from energy an int value between 1 and 9999, with a minimal step of 1OO between each
        int a = (int) (1200 * Math.log(e*1000) - 1930);
        // get from model, particle and source organ a unique int value
        int b = m+p+s;
        // make a unique number from all that
        int computedSeed = 10000*b + a;

        // convert to string and return result
        String seed_as_string = Integer.toString(computedSeed);
        return seed_as_string;

    }

    private void getOutputs () throws ApiException
    {
        // implement some kind of routine to get all new outputs that have not been downloaded yet
        // ...TBC...
        String jobID = "";
        getOutputsPerExecution(jobID);

    }

    private void getOutputsPerExecution (String jobIdentifier) throws ApiException
    {
        // get the results for given workflow
        Execution execution = vipApi.getExecution(jobIdentifier);
        List results = vipApi.getExecutionResults(jobIdentifier,null);
        // do something with the results
        // ...TBC...
    }


    private void listPipelines () throws ApiException
    {
        // List available pipelines
        List<Pipeline> pipelineList = vipApi.listPipelines(null, null, null);
        System.out.println(pipelineList);
    }


    private void getPipelineInfo (String pipeline) throws ApiException
    {
        // Get info on a given pipeline
        // Allows to know (amongst other things) name and type of expected parameters
        Pipeline pipelineInfo = vipApi.getPipeline(pipeline);
        System.out.println(pipelineInfo);
    }

}