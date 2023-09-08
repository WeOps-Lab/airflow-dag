init-db:
	AIRFLOW_HOME=`pwd` airflow db init
	AIRFLOW_HOME=`pwd` airflow users create --firstname admin --lastname admin --email admin --password admin --username admin --role Admin

start-dev:
	AIRFLOW__CORE__DEFAULT_TIMEZONE=Asia/Shanghai AIRFLOW_HOME=`pwd` nohup airflow webserver -p 18080 &
	AIRFLOW__CORE__DEFAULT_TIMEZONE=Asia/Shanghai AIRFLOW_HOME=`pwd` nohup airflow scheduler &
	AIRFLOW__CORE__DEFAULT_TIMEZONE=Asia/Shanghai AIRFLOW_HOME=`pwd` nohup airflow worker &

stop-dev:
	# use ps -ef kill
	kill -9 `ps -ef | grep airflow | grep -v grep | awk '{print $$2}'`
	rm -Rf ./nohup.out

restart:
	kill -9 `ps -ef | grep airflow | grep -v grep | awk '{print $$2}'` &
	rm -Rf ./nohup.out
	AIRFLOW__CORE__DEFAULT_TIMEZONE=Asia/Shanghai AIRFLOW_HOME=`pwd` nohup airflow webserver -p 18080 &
	AIRFLOW__CORE__DEFAULT_TIMEZONE=Asia/Shanghai AIRFLOW_HOME=`pwd` nohup airflow scheduler &
	AIRFLOW__CORE__DEFAULT_TIMEZONE=Asia/Shanghai AIRFLOW_HOME=`pwd` nohup airflow worker &