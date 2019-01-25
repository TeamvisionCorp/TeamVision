package cn.teamcat.doreamon.controller.tools;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Socket;
import java.net.UnknownHostException;

import org.apache.log4j.Logger;

import cn.teamcat.doreamon.controller.config.TimeoutConfig;

/**
 * socket通信
 * @author Sirui.Zhang
 *
 */
public class SocketHelper {
	private Logger log = Logger.getLogger(SocketHelper.class);
	private Logger logger = Logger.getLogger("agentDetecter");
	
	/**
	 *  发送命令
	 * @param url
	 * @param port
	 * @param cmd
	 * @param expect
	 * @return 
	 * @throws UnknownHostException 
	 * @throws IOException 
	 */
	public boolean sendScoketCmd(String ip,int port,String cmd,String expect){
		boolean socket = false;
		try {
			socket = expect.equals( socket(ip, port, cmd));
		} catch (Exception e) {
			// TODO: handle exception
			e.printStackTrace();
		}
		return socket;
	}
	
	
	public String socket(String url,int port,String cmd) throws UnknownHostException, IOException {
		//建立连接
		String actual = "";
		Socket socket;
		socket = new Socket(url,port);
		PrintWriter pr;
		TimeoutConfig timeout = new TimeoutConfig();
		socket.setSoTimeout(timeout.getSocketTimeout());
		pr = new PrintWriter(socket.getOutputStream());
		BufferedReader buf = new BufferedReader(new InputStreamReader(socket.getInputStream()));
		pr.write(cmd+"\n");
		pr.flush();
		//读取服务器返回的字节数组流
		actual = buf.readLine();
		if (cmd != Constants.ALIVE_CMD) {
			log.info("向'"+url+"'发送命令：'"+cmd+"'");
			log.info("'"+url+"'返回消息：'"+actual+"'");
		}else{
			logger.info("向'"+url+"'发送命令：'"+cmd+"'");
			logger.info("'"+url+"'返回消息：'"+actual+"'");
		}
		pr.close();
		buf.close();
		socket.close();
		return actual;
	} 
	
		
}
