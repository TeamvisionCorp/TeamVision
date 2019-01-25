package com.xracoon.teamcat.driver.step;

import java.io.File;
import java.io.IOException;
import java.security.GeneralSecurityException;
import java.util.Map;

import com.jcraft.jsch.JSchException;
import com.xracoon.teamcat.driver.Driver;
import com.xracoon.teamcat.driver.WebService;
import com.xracoon.teamcat.plugin.DeployInfo;
import com.xracoon.teamcat.plugin.TaskConfig;
import com.xracoon.util.basekit.StringEx;
import com.xracoon.util.basekit.security.auth.Credential;
import com.xracoon.util.basekit.ssh.JschSSHUtil;
import com.xracoon.util.basekit.ssh.SSHUtil;

public abstract class DeployStep extends BuildStep {
	protected long serverId;
	protected DeployInfo deployInfo;
	protected DeployServerInfo serverInfo;
	protected String remotePath;
	protected Credential cred;
	protected SSHUtil sshUtil;
	protected File loalDepoyTempDir;
	protected String remoteDeployTempDir;
	
	public void queryServerInfo() throws Exception{
		//查询Server信息
		serverId=Long.parseLong(stepConf.getParam("deploy_server"));
		serverInfo= WebService.queryDeployServer(serverId);
		if(StringEx.isBlank(serverInfo.getRemoteDir()) || serverInfo.getRemoteDir().trim().equals("/"))
			throw new Exception("invaild server config: RemoteDir ("+serverInfo.getRemoteDir()+")");
		
		TaskConfig config = (TaskConfig) env.get(Driver.ENV_TASKCONFIG);
		if(config.isDeployService()){
			deployInfo=config.getDeployInfo();
			remotePath= deployInfo.getDeployDir();
		}
		remoteDeployTempDir= new File(serverInfo.getRemoteDir(), "t"+config.getTaskId()+"_"+config.getTaskName())
				.toString().replace("\\", "/");
		
		@SuppressWarnings("unchecked")
		Map<String, String> tokens=(Map<String, String>) env.get(Driver.ENV_TOKENS);
		if(config.isDeployService())
			tokens.put(Driver.TOK_DEPLOYPATH, remotePath);
		tokens.put(Driver.TOK_DEPLOYSPACE, remoteDeployTempDir);
		stepConf.resolveTokens(tokens);
		
		//查询Credential
		cred= WebService.queryCredential(serverInfo.getCredentialId());
		sshUtil= getSshUtil(serverInfo.getHost(), serverInfo.getPort(), cred );
		
		loalDepoyTempDir=new File(workspace, "_deploy_files");
		if(!loalDepoyTempDir.exists() )
			loalDepoyTempDir.mkdirs();
	}
	
	protected SSHUtil getSshUtil(String host, int port, Credential cred) throws IOException, GeneralSecurityException, JSchException{
		return new JschSSHUtil(host, port, cred);
	}

	abstract public boolean depoyExec() throws Exception;  
	
	@Override
	public boolean exec() throws Exception {
		queryServerInfo();
		return depoyExec();
	}
}
