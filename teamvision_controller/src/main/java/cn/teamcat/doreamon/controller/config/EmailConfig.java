package cn.teamcat.doreamon.controller.config;

import java.util.List;

import org.apache.ibatis.session.SqlSession;

import cn.teamcat.doreamon.controller.tools.Constants;
import cn.teamcat.doreamon.controller.tools.HttpClientHelperBasic;
import cn.teamcat.doreamon.controller.tools.SessionFactoryUtil;
import net.sf.json.JSONArray;
import net.sf.json.JSONObject;

public class EmailConfig {
	public String mailHost;
	public String mailAuth =Constants.EMAIL_IS_AUTH;
	public String mailUsername;
	public String mailPassword;
	public String mailAddress;
	public String defaultMailRecivers;
	public String defaultRtxRecivers;
	
	public EmailConfig() {
		try {			
		Integer EmailConfigtypeid = 7;
		JSONObject EmailConfigRsp = HttpClientHelperBasic.get(Constants.API.GET_DICCONFIG+EmailConfigtypeid+"/dicconfigs", null);
		JSONArray result = EmailConfigRsp.getJSONArray("result");		
		for (int i = 0; i < result.size(); i++) {
			JSONObject data = result.getJSONObject(i);
			String dataName = data.getString("DicDataName");
			Integer dataValue = data.getInt("DicDataValue");
			if (dataValue == 1) {
				setMailHost(dataName);
				continue;
			}
			if (dataValue == 2) {
				setMailUsername(dataName);
				continue;
			}
			if (dataValue == 3) {
				setMailPassword(dataName);
				continue;
			}
			if (dataValue == 4) {
				setMailAddress(dataName);
				continue;
			}
			if (dataValue == 7) {
				setDefaultMailRecivers(dataName);
				continue;
			}
			
		}
		setMailAddress(getMailUsername() + "@" + getMailAddress());
		setDefaultRtxRecivers(getDefaultMailRecivers().replace("@" + getMailAddress(), ""));
		} catch (Exception e) {
			// TODO: handle exception
		}

	}

	public String getMailHost() {
		return mailHost;
	}

	public void setMailHost(String mailHost) {
		this.mailHost = mailHost;
	}

	public String getMailAuth() {
		return mailAuth;
	}

	public void setMailAuth(String mailAuth) {
		this.mailAuth = mailAuth;
	}

	public String getMailUsername() {
		return mailUsername;
	}

	public void setMailUsername(String mailUsername) {
		this.mailUsername = mailUsername;
	}

	public String getMailPassword() {
		return mailPassword;
	}

	public void setMailPassword(String mailPassword) {
		this.mailPassword = mailPassword;
	}

	public String getMailAddress() {
		return mailAddress;
	}

	public void setMailAddress(String mailAddress) {
		this.mailAddress = mailAddress;
	}

	public String getDefaultMailRecivers() {
		return defaultMailRecivers;
	}

	public void setDefaultMailRecivers(String defaultMailRecivers) {
		this.defaultMailRecivers = defaultMailRecivers;
	}

	public String getDefaultRtxRecivers() {
		return defaultRtxRecivers;
	}

	public void setDefaultRtxRecivers(String defaultRtxRecivers) {
		this.defaultRtxRecivers = defaultRtxRecivers;
	}
	
	
}
