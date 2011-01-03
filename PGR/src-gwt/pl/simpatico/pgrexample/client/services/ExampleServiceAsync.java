package pl.simpatico.pgrexample.client.services;

import com.google.gwt.user.client.rpc.AsyncCallback;

import pl.simpatico.pgrexample.client.vo.ExampleVo2;
import pl.simpatico.pgrexample.client.vo.ExampleVo3;

public interface ExampleServiceAsync {
	
	void sumInts(int a, int b, AsyncCallback cb);
	void subArray(String[] tab, int from, int to, AsyncCallback cb);
	void subObject(ExampleVo2 source, AsyncCallback cb); 
	void loginUser(String userName, String password, AsyncCallback cb);
	void logout(AsyncCallback cb);
}
