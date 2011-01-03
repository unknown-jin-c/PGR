package pl.simpatico.pgrexample.client.vo;

public class ExampleVo2 extends ExampleVo1{
	private ExampleVo3 objField;
	

	public void setObjField(ExampleVo3 objField) {
		this.objField = objField;
	}

	public ExampleVo3 getObjField() {
		return objField;
	}
	
	public String toString() {
		return "ExampleVo2: {strField: '" +getStrField() + "', intField: " +getIntField() +"}";
	}
}
