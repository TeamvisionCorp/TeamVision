package com.xracoon.teamcat.driver;

import java.util.Date;

public interface AgentNotifier {
	boolean reportCaseStatus(Long caseId,String caseName, Date start, Date end, int result, String error, String trace); 
	boolean requestArchive(String antStyleFilter, int type);
}
