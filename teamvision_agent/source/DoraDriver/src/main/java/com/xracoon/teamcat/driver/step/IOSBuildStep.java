package com.xracoon.teamcat.driver.step;

import java.io.File;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import com.xracoon.teamcat.driver.BuildTools;
import com.xracoon.teamcat.driver.Driver;
import com.xracoon.util.basekit.system.ExecStatus;
import com.xracoon.util.basekit.system.OS;

public abstract class IOSBuildStep extends BuildStep {
	protected int changeXCodeVersion(String xcode) throws Exception{
		BuildTools bt=(BuildTools) env.get(Driver.ENV_BUILDTOOLS);

		File xcodePath=bt.getXcodePath(xcode);
		if(xcodePath!=null)
			this.xcodeSwitch(xcodePath);
		
		int curVer=-1;
		ExecStatus es=OS.getSingleton().execSyn("xcodebuild -version", null, new File(workspace));
		Matcher m=Pattern.compile("Xcode (\\d+)").matcher(es.getLog()+"");
		if(m.find())
			curVer= Integer.parseInt(m.group(1));
		if(xcodePath==null || Integer.parseInt(xcode.substring(xcode.indexOf("-")+1))==curVer)
			return curVer;

		throw new Exception("xcodebuild version not match expect: "+xcode);
	}

	@Override
	public abstract boolean exec() throws Exception;
}
