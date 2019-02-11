
import org.carmin.client.*;
import org.carmin.client.api.DefaultApi;
import org.carmin.client.model.Execution;
import org.carmin.client.model.Path;
import org.carmin.client.model.Pipeline;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileWriter;
import java.io.IOException;
import java.text.SimpleDateFormat;
import java.util.*;
import java.text.DateFormat;

/**
 * Created by gmathieu
 * Based on a squeleton file Created by abonnet on 4/23/18.
 */

public class OpenDoseClientClass {

    public static void main(String[] args) throws ApiException {

        /********** INIT VARIABLES AND INPUTS ***********/

        // execution date
        DateFormat daytime = new SimpleDateFormat("yyyy-MM-dd_HHmmss");
        Date today = Calendar.getInstance().getTime();
        String reportDate = daytime.format(today);

        // get different lists from config file (in a very, very ugly way)
        Scanner sconfig = null;
        try {
            sconfig = new Scanner(new File("/home/gate/opendose/tests2018-09/GateCLforOpenDose_config/GateCLforOpenDose_config.txt"));
        } catch (FileNotFoundException e) {
            System.out.println("can't open config file");
            e.printStackTrace();
        }
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
        // Name of the MAC file to be used
        String macFileName = sconfig.next();
        sconfig.close();


        // path to the local log file to which we will write execution report
        String reportFilePathName = "/home/gate/opendose/tests2018-09/exec_log_"+reportDate+".txt";
        // LFN of the input zip archive
        String gateInputLFN = "/vip/Home/OpenDose/input/OpenDoseInputData2018-11-14.zip";
        // Path to the gate release to be used (on CVMFS)
        //String gateReleasePath="/cvmfs/biomed.egi.eu/vip/gate/gate_release_8.1";
        //String gateReleasePath="/home/biomedsgm/cvmfs_repo/vip/gate/gate_release_8.1.p01_52f1dd0";
        String gateReleasePath="/cvmfs/biomed.egi.eu/vip/gate/gate_release_8.1.p01_52f1dd0";
        // output directory on VIP
        String outputDir ="/vip/Home/OpenDose/output";

        // build list of source organs from input data
        ArrayList<String> organsList = new ArrayList<String>();
        Scanner s1 = null;
        try {
            s1 = new Scanner(new File(organsListPathName));
        } catch (FileNotFoundException e) {
            System.out.println("can't open organs list input file");
            e.printStackTrace();
        }
        while (s1.hasNextLine()){
            organsList.add(s1.nextLine());
        }
        s1.close();

        // build list of particle types
        //ArrayList<String> particlesList = new ArrayList<String>();
        //particlesList.add ("gamma");
        //particlesList.add ("e-");

        // build list of energy levels from input data
        ArrayList<String> energiesList = new ArrayList<String>();
        Scanner s2 = null;
        try {
            s2 = new Scanner(new File(energiesListPathName));
        } catch (FileNotFoundException e) {
            System.out.println("can't open energies list input file");
            e.printStackTrace();
        }
        while (s2.hasNextLine()){
            energiesList.add(s2.nextLine());
        }
        s2.close();


        /********** CREATE LOCAL LOG FILE ***********/
        File clientExecutionLog = new File(reportFilePathName);
        try{
            clientExecutionLog.createNewFile();
        } catch (IOException e) {
            System.out.println("unable to create local log file");
            e.printStackTrace();
        }

        /********** INIT API CLIENT ***********/
        ApiClient vipApiClient = new ApiClient();
        vipApiClient.setApiKey("l6uf3opn55b5ltrkok6pd7olll");// Key GM
        //vipApiClient.setBasePath("http://vip.creatis.insa-lyon.fr/rest");
        vipApiClient.setBasePath("http://vip.creatis.insa-lyon.fr/vip-1.24-test/rest");
        DefaultApi vipApi = new DefaultApi(vipApiClient);


        /********** PRELIMINARY TEST ***********/

        // List available pipelines
        //List<Pipeline> pipelineList = vipApi.listPipelines(null, null, null);
        //System.out.println(pipelineList);

        // Get info on a given pipeline (here: GateCLforOpenDose/v0.1.0)
        // Allows to know (amongst other things) name and type of expected parameters
        //Pipeline pipelineInfo = vipApi.getPipeline("GateCLforOpenDose%2Fv0.1.0");
        //System.out.println(pipelineInfo);


        try {
            /********** INITIALIZE LOCAL LOG FILE ***********/

            FileWriter writer = new FileWriter(clientExecutionLog);
            writer.write("OPENDOSE EXECUTION REPORT - " + reportDate + "\n\n");
            writer.write("used MAC file: " + macFileName + "\n");
            writer.write("used list of organs: " + organsListPathName + "\n");
            writer.write("used list of energies: " + energiesListPathName + "\n");
            writer.write("number of primaries: " + numberOfPrimaries + "\n");
            writer.write("used input file for gate: " + gateInputLFN + "\n");
            writer.write("used gate release: " + gateReleasePath + "\n");
            writer.write("\n---BEGIN---\n");

            /********** SET PIPELINE AND LAUNCH EXECUTION ***********/

            // Create directory and upload input zip file (already done through the portal)
            //vipApi.createDirectory("/vip/Home/OpenDose/input/");
            //vipApi.uploadPathBinary(gateInputLFN, new File("/home/gate/opendose/tests2018-09/OpenDoseInputData.zip"));

            String executionName    = new String();
            Date nowdate = new Date();
            String nowFormatted = new String();

            Execution execution = new Execution();
            execution.setPipelineIdentifier("GateCLforOpenDose/v0.2.0");

            Map<String, Object> inputValues = new HashMap<>();

            inputValues.put("indata", gateInputLFN);
            inputValues.put("gatereleasepath", gateReleasePath);
            inputValues.put("nbprimaries", numberOfPrimaries);
			inputValues.put("macfile", macFileName);
			inputValues.put("results-directory", outputDir);
            //inputValues.put("CPUestimation", "1");
            //inputValues.put("ParallelizationType", "static");

            // loop over all organs found in input matrix
            //for (String organ : organsList) {
                //inputValues.put("organid", organ);
                inputValues.put("organid", organsList);
                // pass the particle type
                inputValues.put("particletype", particle);
                // pass the list of energies
                inputValues.put("energy", energiesList);
                // set name of execution
                executionName = "OpenDose_PROD_064-AM-L" + "_" + particle + "_" + numberOfPrimaries;
                System.out.println(executionName);
                // setup and launch execution
                execution.setInputValues(inputValues);
                execution.setName(executionName);
                execution = vipApi.initExecution(execution);
                String jobIdentifier = execution.getIdentifier();
                System.out.println(jobIdentifier);
                nowdate= Calendar.getInstance().getTime();
                nowFormatted  = daytime.format(nowdate);
                writer.write(nowFormatted + " : " + executionName + " - " + jobIdentifier + "\n");
                //System.out.println(vipApi.getExecutionResults(jobIdentifier,null));
                //List results = vipApi.getExecutionResults("workflow-fXwrHI",null);
                //execution = vipApi.getExecution("workflow-fXwrHI");

            //}
            writer.write("---END---");
            writer.close();
        } catch (IOException e) {
			System.out.println("Oops, something went wrong. Can't tell you what or why, but you'll figure out I guess.");
            e.printStackTrace();
        }
    }
}
