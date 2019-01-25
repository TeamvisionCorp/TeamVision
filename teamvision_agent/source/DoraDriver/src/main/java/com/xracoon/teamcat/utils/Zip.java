package com.xracoon.teamcat.utils;

import java.io.*;
import java.util.zip.ZipEntry;
import java.util.zip.ZipInputStream;
import java.util.zip.ZipOutputStream;

import com.xracoon.util.basekit.StreamsEx;

public class Zip {
	public static void unzip(String zipfile, String suffix, OutputStream os) throws IOException{
		ZipInputStream zis=null;
		try{
			zis = new ZipInputStream(new FileInputStream(zipfile));
			ZipEntry entry;
			while ((entry = zis.getNextEntry()) != null){
				if(entry.getName().endsWith(suffix)){
					StreamsEx.copy(zis, os);
					break;
				}
		    }
		}finally{
			if(zis!=null)
				zis.close();
		}
	}

	public static void zipDIR(String sourceDIR, String targetZipFile) {
		try {
			FileOutputStream target = new FileOutputStream(targetZipFile);
			ZipOutputStream out = new ZipOutputStream(new BufferedOutputStream(target));
			int BUFFER_SIZE = 1024;
			byte buff[] = new byte[BUFFER_SIZE];
			File dir = new File(sourceDIR);
			if (!dir.isDirectory()) {
				throw new IllegalArgumentException(sourceDIR+" is not a directory!");
			}
			File files[] = dir.listFiles();
			for (int i = 0; i < files.length; i++) {
				FileInputStream fi = new FileInputStream(files[i]);
				BufferedInputStream origin = new BufferedInputStream(fi);
				ZipEntry entry = new ZipEntry(files[i].getName());
				out.putNextEntry(entry);
				int count;
				while ((count = origin.read(buff)) != -1) {
					out.write(buff, 0, count);
				}
				origin.close();
			}
			out.close();
		} catch (IOException e) {
			throw new RuntimeException(e);
		}
	}
}
