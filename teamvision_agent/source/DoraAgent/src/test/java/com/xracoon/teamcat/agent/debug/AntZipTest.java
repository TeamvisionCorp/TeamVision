package com.xracoon.teamcat.agent.debug;
import org.apache.tools.ant.BuildException;
import org.junit.Test;

import com.xracoon.teamcat.agent.file.AntZipUtil;

public class AntZipTest {
	@Test
	public void testZip01() throws BuildException, Exception
	{
		String srcPathname = "D:\\log";
		String zipFilepath = "D:\\log2\\myzip.zip";
		String includes = "*.txt,*.log";
		String excludes = "*.html";
		AntZipUtil.zip(srcPathname, zipFilepath, includes, excludes,null);
	}
}
