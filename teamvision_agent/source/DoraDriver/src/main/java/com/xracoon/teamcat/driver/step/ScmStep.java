package com.xracoon.teamcat.driver.step;

import java.io.File;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

import com.xracoon.teamcat.driver.Driver;
import com.xracoon.teamcat.driver.WebService;
import com.xracoon.teamcat.utils.scm.Revision;
import com.xracoon.teamcat.utils.scm.ScmUtil;
import com.xracoon.util.basekit.StringEx;
import com.xracoon.util.basekit.security.auth.Credential;

public class ScmStep extends BuildStep {

	@Override
	public boolean exec() {
		Credential cred=null;
		try{
			Integer scmIdx= null;
			try{ 
				scmIdx=(Integer) env.remove(Driver.ENV_SCMSTEPIDX);
			}catch(Exception e){
				logger.warn("failed to query scm idx: "+e.getMessage());
			}
			String localPath= stepConf.getParam("local_directory");
			String repo=stepConf.getParam("repository_url");
			
			File file=new File(env.get(Driver.ENV_WORKSPACE).toString());
	
			if(!StringEx.isBlank(localPath) && !localPath.trim().matches("\\.[/\\\\]*"))
				file= new File(file, localPath).getAbsoluteFile();
			cred=WebService.queryCredential(Integer.parseInt(stepConf.getParam("ci_credentials")));
			String strategyKey=(stepConf.getType()==StepType.SCM_GIT?"git":"svn")+"_check_out_strategy";
			int strategy= Integer.parseInt(stepConf.getParam(strategyKey));
			
			String branchOrVersion=stepConf.getParam("branch");
			if(stepConf.getType()==StepType.SCM_SVN && repo.matches(".*@[^/\\\\]+$")){
				int idx=repo.lastIndexOf("@");
				branchOrVersion=repo.substring(idx+1);
				repo=repo.substring(0, idx);
			}
			
			ScmUtil scm=ScmUtil.getScm(repo, branchOrVersion, file.toString(), cred.getUser(), cred.getPasswd(), strategy);
			scm.setLogger(logger);
			
			boolean ret=scm.exec();
			if(!ret){
				logger.error("scm operation failed!");
				return false;
			}
//			//获取lastVersion
//			String lastVersion="";
//			String[] infos=new String[2];
//			infos[0]=scm.getVersion();
			
			//String repo_key=repo+(stepConf.getType()==StepType.SCM_GIT?"/"+stepConf.getParam("branch"):"");
			
			@SuppressWarnings("unchecked")
			Map<String, String> scmVersions = (Map<String, String>) env.get(Driver.ENV_VERSIONMAP);
			@SuppressWarnings("unchecked")
			Map<String, List<Revision>> scmChanges = (Map<String, List<Revision>>) env.get(Driver.ENV_CHANGESET);
			if(scmVersions==null){
				scmVersions=new LinkedHashMap<>();
				env.put(Driver.ENV_VERSIONMAP, scmVersions);
			}
			if(scmChanges==null){
				scmChanges=new LinkedHashMap<>();
				env.put(Driver.ENV_CHANGESET, scmChanges);
			}
			
			@SuppressWarnings("unchecked")			
			Map<String,String> lastVersion= (Map<String,String>)env.get(Driver.ENV_LASTVERSION); //取出上次的版本
			scmVersions.put(repo, scm.getVersion()); //存入现在的最新版本（覆盖上次版本）
			@SuppressWarnings("unchecked")
			Map<String,String> tokens=(Map<String, String>) env.get(Driver.ENV_TOKENS);
			if(!tokens.containsKey(Driver.TOK_SCMVERSION))
				tokens.put(Driver.TOK_SCMVERSION, scm.getVersion());
			if(scmIdx!=null)
				tokens.put(Driver.TOK_SCMVERSION+"_"+scmIdx, scm.getVersion());
			
			if(lastVersion!=null){
				List<Revision> changes=scm.getChangeSet(lastVersion.get(repo));
				if(changes!=null && changes.size()>0)
					scmChanges.put(repo, changes);
			}
			
			return true;
		}catch(Exception e){
			logger.error("exception when handle scm step", e);
			return false;
		}
		finally{
			if(cred!=null)
				cred.clean();
		}
	}
}
