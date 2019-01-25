package com.xracoon.teamcat.driver.step;

import com.xracoon.teamcat.driver.Driver;
import com.xracoon.util.basekit.ArraysEx;
import com.xracoon.util.basekit.StringEx;
import com.xracoon.util.basekit.system.ExecStatus;
import com.xracoon.util.basekit.system.OS;

import java.io.File;

public class ShellPackageStep extends BuildStep {
	@Override
	public boolean exec() throws Exception {
		boolean result=true;
		String workspace=env.get(Driver.ENV_WORKSPACE).toString();
		String cmd=stepConf.getParam("build_command_text");
		String outputFilter=stepConf.getParam("build_target_path");
		String is_clean_outputs=stepConf.getParam("is_clean_outputs");
		String is_upload_file=stepConf.getParam("is_upload_file");
		if(is_clean_outputs !=null)
		{
			this.cleanOutput(outputFilter);	
		}
		
		cmd=StringEx.resolveToken(cmd, ArraysEx.toMap("WORKSPACE", workspace));
		ExecStatus es= OS.getNewInstance().execScriptSyn(cmd, null, new File(workspace));
		if(es.getRetVal()!=0)
			result=false;
        if(is_upload_file!=null)
        {
        	   result=this.archiveFiles(outputFilter, Driver.ARCHIVE_PACKAGE);
        }
        else
        {
        	    result=true;
        }

		return result;
	}
}
