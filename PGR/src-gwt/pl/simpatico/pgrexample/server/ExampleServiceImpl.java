package pl.simpatico.pgrexample.server;

import pl.simpatico.pgrexample.client.services.ExampleService;
import pl.simpatico.pgrexample.client.vo.ExampleVo2;
import pl.simpatico.pgrexample.client.vo.ExampleVo3;

import com.google.gwt.user.server.rpc.RemoteServiceServlet;

public class ExampleServiceImpl extends RemoteServiceServlet implements ExampleService{

	public String[] subArray(String[] tab, int from, int to) {
		int size = to - from;
		String[] newTab = new String[size];
		for (int i = from, k = 0; i < to; i++, k++){
			newTab[k] = tab[i];
		}
		return newTab;
	}

	public ExampleVo3 subObject(ExampleVo2 source) {
		source.getObjField().setIntField(source.getIntField());
		source.getObjField().setStrField(source.getStrField());
		return source.getObjField();
	}

    public boolean loginUser(String userName, String password) {
        if (userName.equals("user") && password.equals("pass")) {
            return true;
        } else if (userName.equals("mng") && password.equals("pass")) {
            return true;
        } else if (userName.equals("adm") && password.equals("pass")) {
            return true;
        }
        return false;  //To change body of implemented methods use File | Settings | File Templates.
    }

    public boolean logout() {
        return false;  //To change body of implemented methods use File | Settings | File Templates.
    }

    public int sumInts(int a, int b) {
		return a + b;
	}

}
