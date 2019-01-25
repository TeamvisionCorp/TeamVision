package com.xracoon.teamcat.agent.device.ddms;

import java.util.ArrayList;
import java.util.Collection;
import java.util.Collections;
import java.util.HashMap;
import java.util.Map;

import org.apache.log4j.Logger;

import com.android.ddmlib.AndroidDebugBridge;
import com.android.ddmlib.AndroidDebugBridge.IDeviceChangeListener;
import com.android.ddmlib.IDevice;
import com.android.ddmlib.IDevice.DeviceState;

/**
 * encapsulation of AndroidDebugBridge
 * @author Yangtianxin
 */
public class AndroidDeviceMonitor {
	private transient Logger logger = Logger.getLogger(AndroidDeviceMonitor.class);
	public void setLogger(Logger logger)
	{
		this.logger=logger;
	}
	
	private AndroidDeviceMonitor(){} 
	private volatile static AndroidDeviceMonitor singleton;  
	public static AndroidDeviceMonitor getInstance() {
		if (singleton == null) {
			synchronized (AndroidDeviceMonitor.class) {
				if (singleton == null) {
					singleton = new AndroidDeviceMonitor();
				}
			}
		}
		return singleton;
	}
	
	private volatile static AndroidDebugBridge bridge;
	private Map<String,IDevice> statusMap=new HashMap<String, IDevice>();
	private AdbDeviceListenerImpl adbDevListener;
	
	public interface IDeviceStateListener {
		void stateChange(String serialNo,IDevice rdev, boolean isOnline);
	}
	private final ArrayList<IDeviceStateListener> sDeviceListeners =new ArrayList<IDeviceStateListener>();
    public synchronized void addDeviceChangeListener(IDeviceStateListener listener) {
        if (!sDeviceListeners.contains(listener)) {
            sDeviceListeners.add(listener);
        }
    }
    public synchronized void removeDeviceChangeListener(IDeviceStateListener listener) {
            sDeviceListeners.remove(listener);
    }
	
    private void deviceStateChange(String serialNo,IDevice rdev, boolean isOnline)
    {
        // because the listeners could remove themselves from the list while processing
        // their event callback, we make a copy of the list and iterate on it instead of
        // the main list.
        // This mostly happens when the application quits.
    	IDeviceStateListener[] listenersCopy = null;
        synchronized (this) {
            listenersCopy = sDeviceListeners.toArray(new IDeviceStateListener[sDeviceListeners.size()]);
        }

        logger.debug(serialNo+"\t"+(isOnline?"online":"offline"));
        
        // Notify the listeners
        for (IDeviceStateListener listener : listenersCopy) {
            // we attempt to catch any exception so that a bad listener doesn't kill our
            // thread
            try {
                listener.stateChange(serialNo,rdev, isOnline);
            } catch (Exception e) {
                logger.error("Error in Listener: "+e.getMessage(), e);
            }
        }
    }
    
    public Collection<IDevice> getOnlineDevices()
    {
    	return Collections.unmodifiableCollection(statusMap.values());
    }
    
	public synchronized void start()
	{
		statusMap.clear();
		adbDevListener=new AdbDeviceListenerImpl();
		AndroidDebugBridge.addDeviceChangeListener(adbDevListener);
		AndroidDebugBridge.init(false);
		bridge= AndroidDebugBridge.createBridge("adb",false);
	}
	
	public synchronized void stop()
	{
		AndroidDebugBridge.removeDeviceChangeListener(adbDevListener);
		AndroidDebugBridge.terminate();
		statusMap.clear();
		bridge=null;
		adbDevListener=null;
	}
	
	private class AdbDeviceListenerImpl implements IDeviceChangeListener
	{
		@Override
		public synchronized void deviceConnected(IDevice device) {
			//logger.info("Device Connected: "+device.getSerialNumber());
			
			if(device.getSerialNumber().equals("????????????"))
				return ;
			
			if(device.getState()==DeviceState.ONLINE)
			{
				statusMap.put(device.getSerialNumber(), device);
				deviceStateChange(device.getSerialNumber(), device,true);
			}
		}

		@Override
		public synchronized void deviceDisconnected(IDevice device) {
			//logger.info("Device Disconnected: "+device.getSerialNumber());
			
			if(device.getSerialNumber().equals("????????????"))
				return ;
			
			statusMap.remove(device.getSerialNumber());
			deviceStateChange(device.getSerialNumber(), device, false);
		}

		@Override
		public synchronized void deviceChanged(IDevice device, int changeMask) {
			//logger.info("Device Changed: "+device.getSerialNumber()+", "+device.getState().toString()+", "+changeMask);
			
			if(device.getSerialNumber().equals("????????????") )
				return ;
			
			if(changeMask==1 )
			{
				if(device.getState()==DeviceState.ONLINE)
				{
					statusMap.put(device.getSerialNumber(), device);
					deviceStateChange(device.getSerialNumber(), device, true);
				}
				else
				{
					statusMap.remove(device.getSerialNumber());
					deviceStateChange(device.getSerialNumber(), device, false);
				}
			}
		}
	}
		
	public static void main(String[] args) throws InterruptedException
	{
		AndroidDeviceMonitor dector=AndroidDeviceMonitor.getInstance();
		dector.start();
		Thread.sleep(10000);
		dector.stop();
	}
}
