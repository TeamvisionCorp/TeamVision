package com.xracoon.teamcat.utils;

import com.google.gson.Gson;

/**
 * Created by GAOZHENBIN on 2017/6/12.
 */
public class GsonHelper {
    private static Gson gson = null;
    private GsonHelper(){

    }
    public static Gson getGson(){
        if(gson==null){
            gson = new Gson();
        }
        return gson;
    }
}
