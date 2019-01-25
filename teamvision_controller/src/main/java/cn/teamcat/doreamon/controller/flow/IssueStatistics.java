package cn.teamcat.doreamon.controller.flow;

import java.util.ArrayList;
import java.util.List;

import org.apache.ibatis.session.SqlSession;
import org.apache.log4j.Logger;

import cn.teamcat.doraemon.controller.db.dict.DatasEnum;
import cn.teamcat.doreamon.controller.config.GlobalConfig;
import cn.teamcat.doreamon.controller.tools.CommonUtil;
import cn.teamcat.doreamon.controller.tools.Constants;
import cn.teamcat.doreamon.controller.tools.HttpClientHelper;
import cn.teamcat.doreamon.controller.tools.SessionFactoryUtil;
import cn.teamcat.doreamon.controller.tools.SocketHelper;
import net.sf.json.JSONObject;
import net.sf.json.JSONArray;
import net.sf.json.JSONObject;
import com.google.gson.JsonArray;
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;
import com.google.zxing.Result;
import com.mysql.fabric.Response;
import com.google.gson.Gson;

/**
 * IssueStatistics Bug统计
 * 
 * @author Siyuan.Lu
 *
 */
public class IssueStatistics {
	Logger log = Logger.getLogger("issueStatistics");
	HttpClientHelper http = new HttpClientHelper();
	CommonUtil time = new CommonUtil();
	GlobalConfig config = new GlobalConfig();

	/**
	 * IssueStatistics
	 * 
	 * @throws Exception
	 */
	public void issueStatistics() throws Exception {
		log.info("IssueStatistics-开始运行");
		issueDailyStatistics();
		issueVersionStatistics();
		log.info("IssueStatistics-运行完毕");
	}

	/**
	 * 每日问题统计
	 * 
	 * @param
	 * @throws Exception
	 */
	private void issueDailyStatistics() throws Exception {
		// 统计有多少个项目需要统计Bug。
		List<Integer> idList = getStasticProjectid();
		log.info("need_dailystatistic_idList  " + idList);
		log.info("idList size:" + idList.size());
		for (int i = 0; i < idList.size(); i++) {
			Integer projectid = idList.get(i);
			JSONArray all_versions = getProjectVersion(projectid);
			log.info("all_versions " + all_versions);
			if (all_versions.size() > config.getIssueVersionlimited()) {
				for (int j = all_versions.size() - config.getIssueVersionlimited(); j < all_versions.size(); j++) {
					Integer versionid = all_versions.getJSONObject(j).getInt("id");
					log.info("versionid  " + versionid);
					insertDailyStatistics(projectid, versionid);
					log.info("已执行插入判断");
				}
			} else {
				for (int j = 0; j < all_versions.size(); j++) {
					Integer versionid = all_versions.getJSONObject(j).getInt("id");
					log.info("versionid  " + versionid);
					insertDailyStatistics(projectid, versionid);
					log.info("已执行插入判断");
				}
			}
		}
	}

	// 获取需要统计的projectList
	private List<Integer> getStasticProjectid() throws Exception {
		JSONObject projectList = http.getProjectList();
		JSONArray projectresult = projectList.getJSONArray("result");
		List<Integer> List = new ArrayList<Integer>();
		for (int i = 0; i < projectresult.size(); i++) {
			Integer id = projectresult.getJSONObject(i).getInt("id");
			JSONObject issuelist = http.getProjectIssuebyIdVersion(id, 0);
			JSONArray issueresult = issuelist.getJSONArray("result");
			if (issueresult.size() > 0) {
				List.add(id);
			}
		}
		return List;
	}

	// 获取project versionList
	private JSONArray getProjectVersion(Integer id) {
		JSONObject projectVersionList = null;
		try {
			projectVersionList = http.getProjectVersionList(id);
		} catch (Exception e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		JSONArray all_versions = projectVersionList.getJSONObject("result").getJSONArray("all_versions");
		return all_versions;
	}

	// 向dailyStatistics表插入数据
	private void insertDailyStatistics(Integer projectid, Integer versionid) {
		try {
			String datetaday = time.getUTCTimeStr(0);
			JSONObject dailyStistics = http.getdaily_statisticsbydate(datetaday, projectid, versionid);
			JSONArray dailyresult = dailyStistics.getJSONArray("result");
			if (dailyresult.size() > 0) {
				// dailyStatistics update
				Integer dailyStatistic = dailyStistics.getJSONArray("result").getJSONObject(0).getInt("id");
				log.info("更新数据！");
				http.dailyStatisticsupdate(projectid, versionid, dailyStatistic);
			} else {
				// dailyStatistics insert
				log.info("插入数据!");
				http.dailyStatisticsinsert(projectid, versionid);
			}
		} catch (Exception e) {
			log.info("get dailyStatistic infomation error");
			e.printStackTrace();
		}
	}

	// 按维度统计Bug，向version_statistics插入数据
	private void issueVersionStatistics() throws Exception {
		// 统计有多少个项目需要统计Bug。
		List<Integer> idList = getStasticProjectid();
		log.info("need_versionstatistic_idList  " + idList);
		log.info("idList size:" + idList.size());
		for (int i = 0; i < idList.size(); i++) {
			Integer projectid = idList.get(i);
			JSONArray all_versions = getProjectVersion(projectid);
			log.info("all_versions " + all_versions);
			if (all_versions.size() > config.getIssueVersionlimited()) {
				for (int j = all_versions.size() - config.getIssueVersionlimited(); j < all_versions.size(); j++) {
					Integer versionid = all_versions.getJSONObject(j).getInt("id");
					log.info("versionid  " + versionid);
					startinsertversionStatistics(projectid, versionid);
					log.info("已执行version_statistics插入版本判断");
				}
			} else {
				for (int j = 0; j < all_versions.size(); j++) {
					Integer versionid = all_versions.getJSONObject(j).getInt("id");
					log.info("versionid  " + versionid);
					startinsertversionStatistics(projectid, versionid);
					log.info("已执行version_statistics插入版本判断");
				}
			}
		}
	}

	// 统一执行插入操作
	private void startinsertversionStatistics(Integer projectid, Integer versionid) {
		insertversionStatisticsSeverity(projectid, versionid, DatasEnum.DimensionSeverity.getValue());
		insertversionStatisticsCategory(projectid, versionid, DatasEnum.DimensionCategory.getValue());
		insertversionStatisticsResolvedType(projectid, versionid, DatasEnum.DimensionResolvedType.getValue());
		insertversionStatisticsModule(projectid, versionid, DatasEnum.DimensionModule.getValue());
	}

	// 向versionStatistics表插入Severity数据
	private void insertversionStatisticsSeverity(Integer projectid, Integer versionid, Integer Dimension) {
		try {
			JSONObject IssueSeverity = http.getissue_severities();
			JSONArray severity = IssueSeverity.getJSONArray("result");
			for (int i = 0; i < severity.size(); i++) {
				Integer sverities = severity.getJSONObject(i).getInt("Value");
				JSONObject versionStistics = http.getdversion_statisticsbyDimbyDimvalue(projectid, versionid,
						Dimension, sverities);
				JSONArray versionresult = versionStistics.getJSONArray("result");
				if (versionresult.size() > 0) {
					// versionStatistics update
					Integer versionStisticsid = versionStistics.getJSONArray("result").getJSONObject(0).getInt("id");
					log.info("Dimension(1)severities更新数据！");
					http.versionStatisticsupdate(projectid, versionid, versionStisticsid,
							Dimension, sverities);
				} else {
					// versionStatistics insert
					log.info("Dimension(1)severities插入数据!");
					http.versionStatisticsinsert(projectid, versionid, Dimension,
							sverities);
				}
			}
		} catch (Exception e) {
			log.info("get dailyStatistic infomation error");
			e.printStackTrace();
		}
	}

	// 向versionStatistics表插入Category数据
	private void insertversionStatisticsCategory(Integer projectid, Integer versionid, Integer Dimension) {
		try {
			JSONObject Issuecatergories = http.getissue_catergories();
			JSONArray catergories = Issuecatergories.getJSONArray("result");
			for (int i = 0; i < catergories.size(); i++) {
				Integer catergoriesvalue = catergories.getJSONObject(i).getInt("Value");
				JSONObject versionStistics = http.getdversion_statisticsbyDimbyDimvalue(projectid, versionid,
						Dimension, catergoriesvalue);
				JSONArray versionresult = versionStistics.getJSONArray("result");
				log.info("!!!!!!!!1"+versionStistics);
				log.info("~~~~~~~~~~~~~~~~~~"+versionresult.size());
				if (versionresult.size() > 0) {
					// versionStatistics update
					Integer versionStisticsid = versionStistics.getJSONArray("result").getJSONObject(0).getInt("id");
					log.info("Dimension(2)category更新数据！");
					http.versionStatisticsupdate(projectid, versionid, versionStisticsid,
							Dimension, catergoriesvalue);
				} else {
					// versionStatistics insert
					log.info("Dimension(2)category插入数据!");
					http.versionStatisticsinsert(projectid, versionid, Dimension,
							catergoriesvalue);
				}
			}
		} catch (Exception e) {
			log.info("get dailyStatistic infomation error");
			e.printStackTrace();
		}
	}

	// 向versionStatistics表插入ResolvedType数据
	private void insertversionStatisticsResolvedType(Integer projectid, Integer versionid, Integer Dimension) {
		try {
			JSONObject Issueresolvedtypes = http.getissue_resolvedtypes();
			JSONArray resolvedtypes = Issueresolvedtypes.getJSONArray("result");
			for (int i = 0; i < resolvedtypes.size(); i++) {
				Integer resolvedtype = resolvedtypes.getJSONObject(i).getInt("Value");
				JSONObject versionStistics = http.getdversion_statisticsbyDimbyDimvalue(projectid, versionid,
						Dimension, resolvedtype);
				JSONArray versionresult = versionStistics.getJSONArray("result");
				if (versionresult.size() > 0) {
					// versionStatistics update
					Integer versionStisticsid = versionStistics.getJSONArray("result").getJSONObject(0).getInt("id");
					log.info("Dimension(3)resolvedtype更新数据！");
					http.versionStatisticsupdate(projectid, versionid, versionStisticsid,
							Dimension, resolvedtype);
				} else {
					// versionStatistics insert
					log.info("Dimension(3)resolvedtype插入数据!");
					http.versionStatisticsinsert(projectid, versionid, Dimension,
							resolvedtype);
				}
			}
		} catch (Exception e) {
			log.info("get dailyStatistic infomation error");
			e.printStackTrace();
		}
	}

	// 向versionStatistics表插入Module数据
	private void insertversionStatisticsModule(Integer projectid, Integer versionid, Integer Dimension) {
		try {
			JSONObject issuemodule = http.getissue_projectmodule(projectid);
			JSONArray issuemodulelist = issuemodule.getJSONArray("result");
			for (int i = 0; i < issuemodulelist.size(); i++) {
				Integer issuemoduleid = issuemodulelist.getJSONObject(i).getInt("id");
				JSONObject versionStistics = http.getdversion_statisticsbyDimbyDimvalue(projectid, versionid,
						Dimension, issuemoduleid);
				JSONArray versionresult = versionStistics.getJSONArray("result");
				if (versionresult.size() > 0) {
					// versionStatistics update
					Integer versionStisticsid = versionStistics.getJSONArray("result").getJSONObject(0).getInt("id");
					log.info("Dimension(4)Module更新数据！");
					http.versionStatisticsupdate(projectid, versionid, versionStisticsid,
							Dimension, issuemoduleid);
				} else {
					// versionStatistics insert
					log.info("Dimension(4)Module插入数据!");
					http.versionStatisticsinsert(projectid, versionid, Dimension, 
							issuemoduleid);
				}
			}
		} catch (Exception e) {
			log.info("get dailyStatistic infomation error");
			e.printStackTrace();
		}
	}
}

