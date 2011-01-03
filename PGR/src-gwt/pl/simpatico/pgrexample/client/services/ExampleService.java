package pl.simpatico.pgrexample.client.services;

import com.google.gwt.user.client.rpc.RemoteService;

import pl.simpatico.pgrexample.client.vo.*;

public interface ExampleService extends RemoteService{
	
	int sumInts(int a, int b);
	String[] subArray(String[] tab, int from, int to);
	ExampleVo3 subObject(ExampleVo2 source);
	
	
	boolean loginUser(String userName, String password);
	boolean logout();

}
