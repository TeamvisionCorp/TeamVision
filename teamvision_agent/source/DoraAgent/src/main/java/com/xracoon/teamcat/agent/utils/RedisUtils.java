package com.xracoon.teamcat.agent.utils;

import com.xracoon.teamcat.agent.webservice.AgentWebService;
import redis.clients.jedis.Jedis;
import redis.clients.jedis.JedisPool;
import redis.clients.jedis.JedisPoolConfig;

import java.util.HashMap;

public class RedisUtils {
    public static JedisPool jedisPool;
    static {
        JedisPoolConfig config = new JedisPoolConfig();
        config.setMaxTotal(50);
        config.setMaxIdle(5);
        config.setMaxWaitMillis(3000);
        HashMap<String,String> map= AgentWebService.getRedisConf();
        jedisPool = new JedisPool(config, map.get("RedisAddress"),Integer.parseInt(map.get("RedisPort")));
    }

    public static boolean set(String key,String value) throws Exception{
        Jedis jedis=null;
        try{
            jedis = jedisPool.getResource();
            jedis.set(key,value);
            return true;
        }catch (Exception e){
            e.printStackTrace();
            return false;
        }finally {
            if(jedis!=null){
                jedis.close();
            }
        }
    }
}
