예외처리(Exception)

예외상황을 인정하고 프로세스를 종료시키는것(해결하는게 아님)
예외상황이 나온다면 이미 정상기능은 힘든상태

예외처리란 try , catch 문을 쓰는 것
ex)
try
{
  문제될것들
}
catch(ArithmeticException e)
{
  System.out.println("오류입니다")
}
--------------------------------------------

      Throwable (모든 예외의 상위 클래스)

Error        Exception

            RuntimeException

Error 클래스:
프로그램이 복구할 수 없는 심각한 오류를 나타냄
주로 시스템 레벨에서 발생하며, 개발자가 직접 처리하기 보다는 시스템 수준에서 처리
일반적으로 발생한 경우에는 프로그램이 종료
예시: OutOfMemoryError, StackOverflowError 등

Exception 클래스:
예외 처리가 가능한(recoverable) 예외를 나타냄
개발자가 예외 처리를 강제로 할 수 있다
예외가 발생할 수 있는 상황을 미리 예측하고 처리할 수 있도록함
Exception 클래스를 상속한 클래스들은 대부분 컴파일러가 강제로 예외 처리를 요구
예시: IOException, SQLException 등

RuntimeException 클래스:
프로그램의 오류나 잘못된 사용에 의해 발생하는 예외
예외 처리가 선택 사항
개발자가 코드에서 미리 예외를 처리할 필요가 없으며, 런타임 시에 발생한 예외를 처리할 수 있다.
RuntimeException 클래스를 상속한 클래스들은 컴파일러가 예외 처리를 강제하지 않는다.
예시: NullPointerException, ArrayIndexOutOfBoundsException 등


