package com.xracoon.teamcat.driver.step;

import java.io.File;

import com.xracoon.teamcat.driver.Driver;
import com.xracoon.util.basekit.system.ExecStatus;
import com.xracoon.util.basekit.system.OS;

public class ShellStep extends BuildStep {
	@Override
	public boolean exec() throws Exception {
		String workspace=env.get(Driver.ENV_WORKSPACE).toString();
		String cmd=stepConf.getParam("command_text");
		ExecStatus es= OS.getNewInstance().execScriptSyn(cmd, null, new File(workspace));
		if(es.getRetVal()!=0)
			return false;
		return true;
	}
}
