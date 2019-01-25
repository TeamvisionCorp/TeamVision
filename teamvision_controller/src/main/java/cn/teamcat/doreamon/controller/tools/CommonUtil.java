package cn.teamcat.doreamon.controller.tools;

import java.text.DateFormat;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.*;

public class CommonUtil {

	public Date getUTCDate() {
		//1、取得本地时间：    
	    java.util.Calendar cal = java.util.Calendar.getInstance();   
	    //2、取得时间偏移量：    
	    final int zoneOffset = cal.get(java.util.Calendar.ZONE_OFFSET);   
	    //3、取得夏令时差：    
	    final int dstOffset = cal.get(java.util.Calendar.DST_OFFSET);    
	    //4、从本地时间里扣除这些差量，即可以取得UTC时间：    
	    cal.add(java.util.Calendar.MILLISECOND, -(zoneOffset + dstOffset));    
	    return cal.getTime();
	}

	public static String getUTCTimeStr(int id) {
		DateFormat format= new SimpleDateFormat("yyyy-MM-dd") ;
	    StringBuffer UTCTimeBuffer = new StringBuffer();
	    // 1、取得本地时间：
	    java.util.Calendar cal = java.util.Calendar.getInstance(); 
	    // 2、取得时间偏移量：
	    int zoneOffset = cal.get(java.util.Calendar.ZONE_OFFSET);
	    // 3、取得夏令时差：
	    int dstOffset = cal.get(java.util.Calendar.DST_OFFSET);
	    // 4、从本地时间里扣除这些差量，即可以取得UTC时间：
	    cal.add(java.util.Calendar.MILLISECOND, -(zoneOffset + dstOffset));
	    cal.add(cal.DATE,id);
	    int year = cal.get(Calendar.YEAR);
	    int month = cal.get(Calendar.MONTH)+1;
	    int day = cal.get(Calendar.DAY_OF_MONTH);
/*	    int hour = cal.get(Calendar.HOUR_OF_DAY);
	    int minute = cal.get(Calendar.MINUTE);*/

	    UTCTimeBuffer.append(year).append("-").append(month).append("-").append(day) ;
	    ;
	    try{
	    	format.parse(UTCTimeBuffer.toString()) ;
	      return UTCTimeBuffer.toString() ;
	    }catch(ParseException e)
	    {
	      e.printStackTrace() ;
	    }
	    return UTCTimeBuffer.toString();
	  }

}
