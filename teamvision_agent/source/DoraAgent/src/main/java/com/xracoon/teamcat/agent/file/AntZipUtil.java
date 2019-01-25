package com.xracoon.teamcat.agent.file;

import java.io.File;
import java.io.IOException;
import org.apache.tools.ant.BuildException;
import org.apache.tools.ant.Project;
import org.apache.tools.ant.taskdefs.Expand;
import org.apache.tools.ant.taskdefs.Zip;
import org.apache.tools.ant.types.FileSet;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class AntZipUtil {
	private static Logger logger1 = LoggerFactory.getLogger(AntZipUtil.class);
	private final static String encoding = "UTF-8";

	public static void zip(String srcPathname, String zipFilepath,String includes,String excludes, Logger log)
	   throws BuildException, IOException {
		
		Logger uselogger=logger1;
		if(log!=null)
			uselogger=log;
		
	  uselogger.info("compress: "+srcPathname+",  includes: "+includes+",  excludes"+excludes);
	  File file = new File(srcPathname);
	  if (!file.exists())
	   throw new IOException("source file or directory "
	     + srcPathname + " does not exist.");

	  Project proj = new Project();
	  FileSet fileSet = new FileSet();
	  fileSet.setProject(proj);

	  if (file.isDirectory()) 
	  {
		  fileSet.setDir(file);
		  fileSet.setIncludes(includes);
		  fileSet.setExcludes(excludes);
	  } else {
		  fileSet.setFile(file);
	  }

	  Zip zip = new Zip();
	  zip.setProject(proj);
	  zip.setDestFile(new File(zipFilepath));
	  zip.addFileset(fileSet);
	  zip.setEncoding(encoding);
	  zip.execute();
	  
	  uselogger.info("Compress done  ==> "+zipFilepath);
	 }

	 public static void unzip(String zipFilepath, String destDir)
	   throws BuildException, IOException {
	  if (!new File(zipFilepath).exists())
	   throw new IOException("zip file " + zipFilepath
	     + " does not exist.");

	  Project proj = new Project();
	  Expand expand = new Expand();
	  expand.setProject(proj);
	  expand.setTaskType("unzip");
	  expand.setTaskName("unzip");
	  expand.setEncoding(encoding);

	  expand.setSrc(new File(zipFilepath));
	  expand.setDest(new File(destDir));
	  expand.execute();
	 }
}
