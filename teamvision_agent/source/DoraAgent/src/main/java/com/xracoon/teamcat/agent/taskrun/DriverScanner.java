package com.xracoon.teamcat.agent.taskrun;

import java.io.File;
import java.io.FileFilter;
import java.io.IOException;
import java.lang.reflect.Field;
import java.net.JarURLConnection;
import java.net.MalformedURLException;
import java.net.URL;
import java.util.ArrayList;
import java.util.Enumeration;
import java.util.List;
import java.util.Vector;
import java.util.jar.JarEntry;
import java.util.jar.JarFile;

import org.apache.log4j.Logger;

import com.xracoon.teamcat.driver.Driver;

/**
 * 在plugin目录检测Driver类，未调试，暂时不用
 * @author Yangtianxin
 */
public class DriverScanner {
	Logger logger = Logger.getLogger(DriverScanner.class);
	private String driverClassPattern="Driver.class";
	
	private void dumpLoadedClass(ClassLoader loader) throws NoSuchFieldException, SecurityException, IllegalArgumentException, IllegalAccessException
	{
		Class cla = loader.getClass();
        while (cla != ClassLoader.class)
            cla = cla.getSuperclass();
        Field field = cla.getDeclaredField("classes");
        field.setAccessible(true);
        Vector v = (Vector) field.get(loader);
        logger.info(v.size());
        for (int i = 0; i < v.size(); i++) {
            System.out.println(((Class)v.get(i)).getName());
        }
	}
	
	private void enumDriverClass(ClassLoader loader) throws IOException
	{
		List<Class<?>> classList = new ArrayList<Class<?>>();  
		
		Enumeration<URL> urls = loader.getResources("plugins");  
		while (urls.hasMoreElements()) {  
            URL url = urls.nextElement();  
            //logger.info(url.toString());
            if (url != null) {  
                String protocol = url.getProtocol();  
                String pkgPath = url.getPath();  
                //System.out.println("protocol:" + protocol +" path:" + pkgPath);  
                if ("file".equals(protocol)) {  
                    // 本地自己可见的代码  
                    findClassName(classList, pkgPath);  
                } else if ("jar".equals(protocol)) {  
//                    // 引用第三方jar的代码  
                    findJarClassName(classList, url);  
                }  
            }  
        }
	}
	
	private void findClassName(List<Class<?>> clazzList, String pkgPath) throws MalformedURLException, IOException {  
        if(clazzList == null){  
            return;  
        }  
        File[] files = filterClassFiles(pkgPath);// 过滤出.class文件及文件夹  
        System.out.println("files:" +((files == null)?"null" : "length=" + files.length));  
        if(files != null){  
            for (File f : files) {  
                String fileName = f.getName();  
                if(f.isFile() && fileName.toLowerCase().endsWith(".jar"))
                {
                	//logger.info(fileName);
                	findJarClassName(clazzList,new URL("jar:file:/"+f.toString()+"!/"));
                }
//                else if (f.isFile() && fileName.endsWith(driverClassPattern) && fileName.length()>driverClassPattern.length()) {
//                    // .class 文件的情况  
//                	//logger.info(fileName);
//                    //String clazzName = getClassName(pkgName, fileName);  
//                    //addClassName(clazzList, clazzName);  
//                }
                else {  
                    // 文件夹的情况,需要继续查找该文件夹/包名下的类  
                    String subPkgPath = pkgPath +"/"+ fileName;  
                    findClassName(clazzList, subPkgPath);  
                }  
            }  
        }  
    }  
	
	 public void findJarClassName(List<Class<?>> clazzList, URL url) throws IOException
	 {  
	        JarURLConnection jarURLConnection = (JarURLConnection) url.openConnection();  
	        JarFile jarFile = jarURLConnection.getJarFile();  
	        //System.out.println("jarFile:" + jarFile.getName());  
	        Enumeration<JarEntry> jarEntries = jarFile.entries();  
	        while (jarEntries.hasMoreElements()) 
	        {  
	            JarEntry jarEntry = jarEntries.nextElement();  
	            String jarEntryName = jarEntry.getName(); // 类似：sun/security/internal/interfaces/TlsMasterSecret.class  
	            String clazzName = jarEntryName.replace("/", ".");  
	            String classFile=jarEntryName.substring(jarEntryName.lastIndexOf("/")+1);
//	            /System.out.println("jar entryName:" + jarEntryName); 
	            if (classFile.endsWith(driverClassPattern) && classFile.length()>driverClassPattern.length()) 
	            {    
	              //System.out.println("jar entryName:" + jarEntryName);  
	               addClassName(clazzList, jarEntryName);  
	            }  
	        }  
	    }  
	 
	 private void addClassName(List<Class<?>> clazzList, String clazzName) {  
	        if (clazzList != null && clazzName != null) {  
	            Class<?> clazz = null;  
	            try {  
	            	logger.info("loading: "+clazzName);
	                clazz = Class.forName(clazzName);  
	            } catch (ClassNotFoundException e) {  
	                e.printStackTrace();  
	            }  
//	          System.out.println("isAnnotation=" + clazz.isAnnotation() +" author:" + clazz.isAnnotationPresent(author.class));  
	              
	            if (clazz != null && Driver.class.isAssignableFrom(clazz)) {
	            	clazzList.add(clazz);
	            }  
	        }  
	    }  
	 
	 private File[] filterClassFiles(String pkgPath) {  
	        if(pkgPath == null){  
	            return null;  
	        }  
	        // 接收 .class 文件 或 类文件夹  
	        return new File(pkgPath).listFiles(new FileFilter() {  
	            @Override  
	            public boolean accept(File file) {  
	            	String classFile=file.getName().substring(file.getName().lastIndexOf("/")+1);
	                return (file.isFile() && (classFile.endsWith(driverClassPattern) && classFile.length()>driverClassPattern.length()) || file.getName().toLowerCase().endsWith(".jar") )|| file.isDirectory();  
	            }  
	        });  
	    } 
}
