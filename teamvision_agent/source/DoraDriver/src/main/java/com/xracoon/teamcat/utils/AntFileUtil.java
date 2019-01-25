package com.xracoon.teamcat.utils;

import java.io.File;
import java.io.IOException;
import java.util.StringTokenizer;
import org.apache.tools.ant.DirectoryScanner;
import org.apache.tools.ant.Project;
import org.apache.tools.ant.types.FileSet;

public class AntFileUtil {
	
	static public FileSet createFileSet(File baseDir, String includes, String excludes)
	{
		FileSet fs=new FileSet();
		fs.setDir(baseDir);
		fs.setProject(new Project());
		
		StringTokenizer tokens=null;
		if(includes!=null && includes.trim().length()>0)
		{
			tokens=new StringTokenizer(includes,",");
			while(tokens.hasMoreTokens())
			{
				String token=tokens.nextToken().trim();
				fs.createInclude().setName(token);
			}
		}
		if(excludes!=null && excludes.trim().length()>0)
		{
			tokens=new StringTokenizer(excludes,",");
			while(tokens.hasMoreTokens())
			{
				String token=tokens.nextToken().trim();
				fs.createExclude().setName(token);
			}
		}
		
		return fs;
	}
	
	static public File[] listAll(File base, final String incs, final String excs) throws IOException, InterruptedException
	{
    		FileSet fs=createFileSet(base,incs,excs);
    		DirectoryScanner ds=fs.getDirectoryScanner(new Project());
    		String[] files=ds.getIncludedFiles();
    		String[] dirs=ds.getIncludedDirectories();
    		File[] all=new File[files.length+dirs.length];
    		int k=0;
    		for(int i=0; i<files.length; i++,k++)
    			all[k]=new File(base, files[i]);
    		for(int i=0; i<dirs.length; i++,k++)
    			all[k]=new File(base, dirs[i]);
    		return all;
	}
}
