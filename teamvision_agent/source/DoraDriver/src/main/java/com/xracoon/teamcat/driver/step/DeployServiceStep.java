package com.xracoon.teamcat.driver.step;

import java.io.File;
import java.io.FileInputStream;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;

import com.xracoon.teamcat.driver.WebService;
import com.xracoon.teamcat.driver.step.DeployFileStep.DeployFileItem;
import com.xracoon.teamcat.utils.AntFileUtil;
import com.xracoon.teamcat.utils.AntZipUtil;
import com.xracoon.teamcat.utils.HttpUtils;
import com.xracoon.util.basekit.FilesEx;
import com.xracoon.util.basekit.StringEx;

public class DeployServiceStep extends DeployStep {
	
	private File searchDeployFilePath(String fileFilter) throws Exception{
		File deployFile= null;
		try{
			File pathTest=new File(this.workspace, fileFilter);
			if(pathTest.exists())
				deployFile=pathTest;
		}catch(Exception e){ }
		if(deployFile ==null){
			File[] files= AntFileUtil.listAll(new File(this.workspace), fileFilter, null);
			if(files.length==0) throw new Exception("部署文件未找到");
			if(files.length>1) throw new Exception("匹配的部署文件不只一个，无法确定");
			deployFile=files[0];
		}
		return new File(deployFile.getCanonicalPath());
	} 
	
	@Override
	public boolean depoyExec() throws Exception {
		String fileFilter=stepConf.getParam("source_file");
		String remotecmd=stepConf.getParam("exec_command","").replace("\r", "");
		System.out.println(this.deployInfo);
		File deployFile=searchDeployFilePath(fileFilter);
		
		//如果是目录，先压缩
		if(deployFile.isDirectory()){
			File zipFile=new File(this.workspace, deployFile.getName()+".zip");
			if(zipFile.exists())
				zipFile.delete();
			AntZipUtil.zip(deployFile.getAbsolutePath(), zipFile.getAbsolutePath(), null, null, logger);
			deployFile=zipFile;
		}
		
		//clean remoteDeployTempDir, transport deploy file
		String remotefile=new File(remoteDeployTempDir, deployFile.getName()).toString().replace("\\", "/");
		sshUtil.remoteExec("rm -rf "+remoteDeployTempDir+ " && mkdir -p "+remoteDeployTempDir);
		sshUtil.writeFile(new FileInputStream(deployFile), remotefile);
		logger.info("transport file: "+deployFile+ " -> "+ remotefile);
		
		//deploy script
		File localScript=new File(this.loalDepoyTempDir, "deployScript.sh");
		String remoteScript=new File(this.remoteDeployTempDir, "deployScript.sh").toString().replace("\\", "/");
		FilesEx.writeFile(remotecmd, localScript);
		//sshExecutor.remoteExec("rm -f "+remoteScript);
		sshUtil.writeFile(new FileInputStream(localScript), remoteScript);
		logger.info("depoyScript file: "+localScript+ " -> "+ remoteScript);
		sshUtil.remoteExec("chmod 744 "+remoteScript);
		
		//stop service
		if(!StringEx.isBlank(this.deployInfo.getStopCommand()))
			sshUtil.remoteExec(this.deployInfo.getStopCommand());
		
		//clear files
		sshUtil.remoteExec("rm -rf "+this.remotePath+" && mkdir -p "+this.remotePath);
		
		//extract files
		if(deployFile.getName().toLowerCase().endsWith(".war")|| deployFile.getName().toLowerCase().endsWith(".zip")){
			sshUtil.remoteExec("unzip -o -d "+this.remotePath+" "+remotefile);
		}
		
		//replace files
		replaceFiles();

		//run script
		sshUtil.remoteExec(remoteScript);
		
		//start service
		if(!StringEx.isBlank(this.deployInfo.getStartCommand()))
			sshUtil.remoteExec(this.deployInfo.getStartCommand());
		
		return true;
	}
	
	private void replaceFiles() throws Exception{
		List<Long> replaceFiles=new ArrayList<>();
		if(stepConf.getParam("replace_file")!=null)
			replaceFiles.add(Long.parseLong(stepConf.getParam("replace_file")));
		else if(stepConf.getParamMultiValue("replace_file")!=null)
			for(String var : stepConf.getParamMultiValue("replace_file"))
				replaceFiles.add(Long.parseLong(var));
		
		Map<Long, DeployFileItem> allFiles= WebService.queryDeployReplaceFile(deployInfo.getId());
		List<DeployFileItem> fileItems=new ArrayList<>();
		
		for(Long id: replaceFiles)
			if(allFiles.containsKey(id))
				fileItems.add(allFiles.get(id));
		
		for(DeployFileItem f:fileItems){
			if(f.getReplaceTarget()==null || f.getReplaceTarget().equalsIgnoreCase("null"))
				continue;
			
			String url=WebService.baseUrlCI.substring(0,WebService.baseUrlCI.length()-7)+f.getFileUrl().substring(f.getFileUrl().indexOf("/ci/"));
			String localReplacefile=new File(this.loalDepoyTempDir, f.getFileName()).toString();
			String remoteReplacefile=new File(this.remotePath, f.getReplaceTarget()).toString().replace("\\", "/");
			HttpUtils.download(url, localReplacefile);
			sshUtil.writeFile(new FileInputStream(localReplacefile), remoteReplacefile);
			logger.info("replace file: "+localReplacefile+ " -> "+ remoteReplacefile);
		}
	}
}
