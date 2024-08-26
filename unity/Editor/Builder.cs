using UnityEditor;
using UnityEditor.Build.Reporting;
using UnityEngine;
using System.IO;
using System.Collections;
using System.Collections.Generic;


public class Builder
{
    private static void GetAllScenes(string targetDirectory, List<string> fileList)
    {
        string [] fileEntries = Directory.GetFiles(targetDirectory, "*.unity");
        foreach(string fileName in fileEntries){
            fileList.Add(fileName);
        }

        string [] subdirectoryEntries = Directory.GetDirectories(targetDirectory);
        foreach(string subdirectory in subdirectoryEntries)
            GetAllScenes(subdirectory, fileList);
    }

    private static string getSceneName(string searchName) {
        List<string> filenames = new List<string>();
        GetAllScenes("./Assets/", filenames);
        string searchSceneFile = "";
        string sampleSceneFile = "";
        string otherSceneFile = "";
        foreach (string fileName in filenames) {
        	if(!fileName.ToUpper().EndsWith(".UNITY")) continue;
        	
        	Debug.Log("LOOP PRINT: " + fileName);
            if(fileName.ToUpper().Contains(searchName.ToUpper())){
                searchSceneFile = fileName;
                break;
            }
            else if (fileName.ToUpper().EndsWith("SAMPLESCENE.UNITY")){
            	sampleSceneFile = fileName;
            }
            else {
            	otherSceneFile = fileName;
            }
        }

		if(searchSceneFile != "") return searchSceneFile;
        if(sampleSceneFile != "") return sampleSceneFile;
        if(otherSceneFile != "") return otherSceneFile;
        return null;
    }

	public static void BuildProject()
	{
		string sceneName = getSceneName("MainGame");
		Debug.Log($"Using Scene: {sceneName}");
		var options = new BuildPlayerOptions
		{
            scenes = new[] {sceneName,},
			//target = BuildTarget.WebGL, 
			//locationPathName = "./WebGL",
			target = BuildTarget.StandaloneOSX, 
			locationPathName = "./MacOS",
			options = BuildOptions.AutoRunPlayer,
		};

        var report = BuildPipeline.BuildPlayer(options);

        if (report.summary.result == BuildResult.Succeeded)
        {
            Debug.Log($"Build Successful - Scene: {sceneName} Written To:  {options.locationPathName}");
        }
        else if (report.summary.result == BuildResult.Failed)
        {
            Debug.LogError($"Build Failed");
        }
		
	}
}

