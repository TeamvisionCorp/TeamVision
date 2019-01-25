package com.xracoon.teamcat.driver.step.testngsteps;

import com.xracoon.teamcat.driver.Driver;
import com.xracoon.teamcat.driver.WebService;
import com.xracoon.teamcat.driver.step.BuildStep;
import com.xracoon.teamcat.models.ci.CiAutoCase;
import com.xracoon.teamcat.models.ci.CiAutoCaseInfo;
import com.xracoon.teamcat.models.ci.CiTaskBasic;
import com.xracoon.teamcat.utils.testngtools.TestProcessListener;
import com.xracoon.testutil.model.TestCase;
import com.xracoon.testutil.model.TestClass;
import com.xracoon.testutil.model.TestPack;
import com.xracoon.testutil.model.TestSuite;
import com.xracoon.util.basekit.system.OS;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;


public abstract class TestNgStep extends BuildStep{
    @Override
    public final boolean exec() throws Exception {
        initEnv();
        runTest();
        runFinsh();
        return true;
    }

    public abstract void initEnv() throws Exception;
    public abstract boolean runTest() throws Exception;
    public abstract boolean runFinsh() throws Exception;

    public List<TestCase> getTestCaseIdsByCiTaskBasic(CiAutoCaseInfo ciAutoCaseInfo){
        List<TestCase> testCaseList=new ArrayList<>();
        List<CiAutoCase> ciAutoCases=ciAutoCaseInfo.getResult().getResults();
        for(CiAutoCase ciAutoCase:ciAutoCases){
            TestCase testCase=new TestCase(ciAutoCase.getId().longValue(),ciAutoCase.getPackageName(),ciAutoCase.getClassName(),ciAutoCase.getCaseName());
            testCaseList.add(testCase);
        }
        return testCaseList;
    }

    public Map<String,WebService.CaseMapItem> getCaseMapItemByCiAutoCaseInfo(CiAutoCaseInfo ciAutoCaseInfo){
        Map<String, WebService.CaseMapItem> caseMap=null;
        if(ciAutoCaseInfo.getResult().getResults().size()>0){
            caseMap=new HashMap<>();
            for(CiAutoCase ciAutoCase:ciAutoCaseInfo.getResult().getResults()){
                WebService.CaseMapItem caseMapItem=new WebService.CaseMapItem();
                caseMapItem.caseId=ciAutoCase.getId();
                StringBuilder stringBuilder=new StringBuilder();
                stringBuilder.append(ciAutoCase.getClassName());
                stringBuilder.append(".");
                stringBuilder.append(ciAutoCase.getCaseName());
                caseMapItem.caseName=stringBuilder.toString();
                caseMap.put(stringBuilder.toString(),caseMapItem);
            }
        }
        return caseMap;
    }

    protected void prepareHost(int envId) throws Exception{
        OS os=OS.getSingleton();
        //host 查询
        Map<String,String> hostIpMap= WebService.queryHosts(envId);
        if(hostIpMap!=null && hostIpMap.size()>0 && !OS.isMac()){
            os.backupHost("./host.bak");
            os.appendHost(hostIpMap);
            os.checkHosts(hostIpMap);

            logger.info("host prepared");
            for(String k:hostIpMap.keySet()){
                logger.info("- "+hostIpMap.get(k)+"\t"+k);
            }
        }
        else{
            logger.info("no host binding");
        }
    }

    class TestListenerImpl implements TestProcessListener{
        private Map<String, WebService.CaseMapItem> caseIdMap;
        public TestListenerImpl(Map<String, WebService.CaseMapItem> caseIdMap){
            this.caseIdMap=caseIdMap;
        }
        @Override
        public void prepare(TestSuite suite) {
        }

        @Override
        public void start(TestCase tcase) {
        }

        @Override
        public void end(TestCase tcase) throws Exception {
            logger.warn(" -> update case reult: ["+tcase.resultCode+"] "+tcase.getFullName());
            String key=tcase.className+"."+tcase.name;
            WebService.CaseMapItem item= caseIdMap.get(key);
            logger.info(tcase.getFullName());
            if(item!=null){
                WebService.updateCaseResult(Long.parseLong(env.get(Driver.ENV_TESTRESULTID).toString()), tcase.start, tcase.end, tcase.resultCode, tcase.info, tcase.cause,item.caseId);
            }else{ 
                logger.error("case not found : "+key);
            }
//            if(item!=null){
//                logger.warn(" -> update case reult: ["+tcase.resultCode+"] "+tcase.getFullName());
//                WebService.updateCaseResult(item.resultId, tcase.start, tcase.end, tcase.resultCode, tcase.info, tcase.cause);
//            }
//            else{
//                logger.warn(" -> insert case reult: ["+tcase.resultCode+"] "+tcase.getFullName());
//                WebService.updateCaseResult(null, tcase.start, tcase.end, tcase.resultCode, tcase.info, tcase.cause);
//            }
        }

        @Override
        public void start(TestClass tclass) {
        }

        @Override
        public void end(TestClass tclass) {
        }

        @Override
        public void start(TestPack tclass) {
        }

        @Override
        public void end(TestPack tclass) {
        }

        @Override
        public void start(TestSuite tclass) {
        }

        @Override
        public void end(TestSuite tclass) {
        }

        @Override
        public void finish(TestSuite suite) {
        }
    }
}
