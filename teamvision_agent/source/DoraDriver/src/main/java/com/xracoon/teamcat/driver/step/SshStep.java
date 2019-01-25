package com.xracoon.teamcat.driver.step;

import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.util.Arrays;
import java.util.Map;
import org.apache.tools.ant.DirectoryScanner;
import org.apache.tools.ant.Project;
import org.apache.tools.ant.types.FileSet;

import com.xracoon.teamcat.driver.Driver;
import com.xracoon.teamcat.driver.WebService;
import com.xracoon.teamcat.plugin.TaskConfig;
import com.xracoon.teamcat.utils.AntFileUtil;
import com.xracoon.util.basekit.FilesEx;
import com.xracoon.util.basekit.StringEx;

public class SshStep extends DeployStep {
	@Override
	public void queryServerInfo() throws Exception{
		//查询Server信息
		serverId=Long.parseLong(stepConf.getParam("deploy_server"));
		serverInfo= WebService.queryDeployServer(serverId);
		if(StringEx.isBlank(serverInfo.getRemoteDir()) || serverInfo.getRemoteDir().trim().equals("/"))
			throw new Exception("invaild server config: RemoteDir ("+serverInfo.getRemoteDir()+")");
		
		//查询Credential
		cred= WebService.queryCredential(serverInfo.getCredentialId());
		sshUtil= getSshUtil(serverInfo.getHost(), serverInfo.getPort(), cred );
		
		TaskConfig config = (TaskConfig) env.get(Driver.ENV_TASKCONFIG);
		remoteDeployTempDir= new File(serverInfo.getRemoteDir(), "t"+config.getTaskId()+"_"+config.getTaskName())
				.toString().replace("\\", "/");
		this.remotePath=serverInfo.getRemoteDir();
		
		@SuppressWarnings("unchecked")
		Map<String, String> tokens=(Map<String, String>) env.get(Driver.ENV_TOKENS);
		tokens.put(Driver.TOK_DEPLOYPATH, remotePath);
		stepConf.resolveTokens(tokens);
		
		loalDepoyTempDir=new File(workspace, "_ssh_files");
		if(!loalDepoyTempDir.exists() )
			loalDepoyTempDir.mkdirs();
	}
	
	@Override
	public boolean depoyExec() throws Exception {
		String fileFilter=stepConf.getParam("source_file");
		String remotecmd=stepConf.getParam("exec_command","").replace("\r", "");
		String dest_dir= stepConf.getParam("dest_dir");
		String exclude_file=stepConf.getParam("exclude_file");
		
		File[] files=listAll(new File(workspace), fileFilter, exclude_file);
		
		//deploy script
		File localScript=new File(this.loalDepoyTempDir, "sshScript.sh");
		String remoteScript=new File(this.remoteDeployTempDir, "sshScript.sh").toString().replace("\\", "/");
		FilesEx.writeFile(remotecmd, localScript);
		//sshExecutor.remoteExec("rm -f "+remoteScript);
		sshUtil.writeFile(new FileInputStream(localScript), remoteScript);
		logger.info("sshScript file: "+localScript+ " -> "+ remoteScript);
		sshUtil.remoteExec("chmod 744 "+remoteScript);
		
		//replace files
		transferFiles(dest_dir, files);

		//run script
		sshUtil.remoteExec(remoteScript);
		
		return true;
	}
	
	public File[] listAll(File base, final String incs, final String excs) throws IOException, InterruptedException{
		if(StringEx.isBlank(incs) && StringEx.isBlank(excs))
			return new File[0];
		
		FileSet fs=AntFileUtil.createFileSet(base,incs,excs);
		DirectoryScanner ds=fs.getDirectoryScanner(new Project());
		String[] files=ds.getIncludedFiles();
		//String[] dirs=ds.getIncludedDirectories();
		String[] dirs=new String[0];
		File[] all=new File[files.length+dirs.length];
		int k=0;
		for(int i=0; i<files.length; i++,k++)
			all[k]=new File(files[i]);
		for(int i=0; i<dirs.length; i++,k++)
			all[k]=new File(dirs[i]);
		return all;
	}

	private void transferFiles(String dest_dir, File[] files) throws Exception{
		logger.info("transfor files "+Arrays.toString(files));
		File outPath=null;
		if(dest_dir.startsWith("/"))
			outPath=new File(dest_dir);
		else
			outPath=new File(this.remotePath,dest_dir);
			
		for(File f:files){
			File localFile=new File(this.workspace, f.getPath());

			String remotefile=new File(outPath, f.getPath()).toString().replace("\\", "/");
			sshUtil.writeFile(new FileInputStream(localFile), remotefile);
			logger.info("transfer file: "+localFile+ " -> "+ remotefile);
		}
	}
}
