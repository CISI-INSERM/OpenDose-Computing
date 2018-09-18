
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

        // path to the MAC file to be used
        String macFilePathName ="/home/gate/opendose/tests2018-09/InputData/main_AF.mac";
        // path to the file containing the list of source organs to be used as input
        String organsListPathName = "/home/gate/opendose/tests2018-09/InputData/data/ICRP_AF_LabelsToMaterials_TEST.txt";
        // path to the file containing the list of energies to be used as input
        String energiesListPathName = "/home/gate/opendose/tests2018-09/InputData/data/energies_7.dat";
        // path to the local log file to which we will write execution report
        String reportFilePathName = "/home/gate/opendose/tests2018-09/exec_log_"+reportDate+".txt";
        // LFN of the input zip archive
        String gateInputLFN = "/vip/Home/myGateSimus/inputs/GateInputU07.zip";
        // LFN of the gate release to be used
        String gateReleaseLFN="/grid/biomed/creatis/vip/data/groups/GateLab/releases/gate_release_8.1p01_light.tar.gz";
        // Number of primaries for the simulations
        String numberOfPrimaries = "1000";

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
            organsList.add(s1.next());
            s1.nextLine();
        }
        s1.close();

        // build list of particle types
        ArrayList<String> particlesList = new ArrayList<String>();
        particlesList.add ("gamma");
        particlesList.add ("electron");

        // build list of energy levels from input data
        ArrayList<String> energiesList = new ArrayList<String>();
        Scanner s2 = null;
        try {
            s2 = new Scanner(new File(energiesListPathName));
        } catch (FileNotFoundException e) {
            System.out.println("can't open energies list input file");
            e.printStackTrace();
        }
        while (s2.hasNext()){
            energiesList.add(s2.next());
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
        /*
        ApiClient vipApiClient = new ApiClient();
        vipApiClient.setApiKey("l6uf3opn55b5ltrkok6pd7olll");// Key GM
        vipApiClient.setBasePath("http://vip.creatis.insa-lyon.fr/rest");
        DefaultApi vipApi = new DefaultApi(vipApiClient);
        */

        /********** PRELIMINARY TEST ***********/

        // List available pipelines
        /*
        List<Pipeline> pipelineList = vipApi.listPipelines(null, null, null);
        System.out.println(pipelineList);
        */

        // Get info on a given pipeline (here: GateLab/0.4.7)
        // Allows to know (amongst other things) name and type of expected parameters
        /*
        Pipeline pipelineInfo = vipApi.getPipeline("GateLab%2F0.4.7");
        System.out.println(pipelineInfo);
        */


        try {
            /********** INITIALIZE LOCAL LOG FILE ***********/

            FileWriter writer = new FileWriter(clientExecutionLog);
            writer.write("OPENDOSE EXECUTION REPORT - " + reportDate + "\n\n");
            writer.write("used MAC file: " + macFilePathName + "\n");
            writer.write("used list of organs: " + organsListPathName + "\n");
            writer.write("used list of energies: " + energiesListPathName + "\n");
            writer.write("number of primaries: " + numberOfPrimaries + "\n");
            writer.write("used input file for gate: " + gateInputLFN + "\n");
            writer.write("used gate release: " + gateReleaseLFN + "\n");
            writer.write("\n---BEGIN---\n");

            /********** SET PIPELINE AND LAUNCH EXECUTION ***********/

            // Create directory and upload input zip file (alternatively, we can upload an input file through the portal)
            //vipApi.createDirectory("/vip/Home/2018-07-23_GateLabAPITest/");
            //vipApi.uploadPathBinary("/vip/Home/myGateSimus/inputs/GateInputU07.zip", new File("/home/gate/GateInputU07.zip"));

            String executionName    = new String();
            Date nowdate = new Date();
            String nowFormatted = new String();

            /*Execution execution = new Execution();
            execution.setPipelineIdentifier("GateLab/0.4.7"); */

            Map<String, Object> inputValues = new HashMap<>();

            inputValues.put("CPUestimation", "1");
            inputValues.put("GateInput", gateInputLFN);
            inputValues.put("GateRelease", gateReleaseLFN);
            inputValues.put("NumberOfParticles", numberOfPrimaries);
            inputValues.put("ParallelizationType", "static");

            // loop over all organs found in input matrix
            for (String organ : organsList) {
                inputValues.put("organid", organ);
                // loop over all particle types
                for (String particle : particlesList) {
                    inputValues.put("particletype", particle);
                    // loop over all energy levels
                    for (String energy : energiesList) {
                        inputValues.put("energy", energy);
                        executionName = "OpenDose_" + organ + "_" + particle + "_" + energy;
                        inputValues.put("outputfilename", executionName + ".tar.gz");
                        System.out.println(executionName);
                        // setup and launch execution
                        /*execution.setInputValues(inputValues);
                        execution.setName(executionName);
                        execution = vipApi.initExecution(execution);
                        System.out.println(execution.getIdentifier());*/
                        nowdate= Calendar.getInstance().getTime();
                        nowFormatted  = daytime.format(nowdate);
                        writer.write(nowFormatted + " : " + executionName + "\n");
                    }
                }
            }
            writer.write("---END---");
            writer.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
