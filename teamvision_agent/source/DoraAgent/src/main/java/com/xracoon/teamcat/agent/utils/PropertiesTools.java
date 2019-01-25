package com.xracoon.teamcat.agent.utils;

import com.xracoon.teamcat.agent.app.ConsoleLauncher;
import com.xracoon.teamcat.driver.WebService;
import com.xracoon.util.basekit.FilesEx;
import com.xracoon.util.basekit.StringEx;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.File;
import java.io.IOException;
import java.io.InputStream;
import java.util.Properties;

/**
 * Created by GAOZHENBIN on 2017/6/30.
 */
public class PropertiesTools {
    private static Logger logger= LoggerFactory.getLogger(PropertiesTools.class);
    private static InputStream inputStream;
    private static Properties properties=null;

    static{
        try{
            String configFile= ConsoleLauncher.basePath;
            if(StringEx.isBlank(configFile))
                throw new Exception("config file agent.properties not found");
            File file=new File(configFile, "agent.properties");
            //File file=new File("/home/gaozhenbin/workcodes/teamcat_agent/source/DoraAgent/", "agent.properties");
            inputStream= FilesEx.openInputStream(file.getAbsolutePath());
            properties = new Properties();
            properties.load(inputStream);
            inputStream.close();
        }catch(Exception e){
            logger.error("agent.properties load failed");
            e.printStackTrace();
            if(inputStream!=null)
                try {
                    inputStream.close();
                } catch (IOException e1) {
                    e1.printStackTrace();
                }
        }
    }

    public static String getProperty(String key){
        return properties.getProperty(key);
    }
}
