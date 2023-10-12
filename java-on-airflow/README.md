### How to build the Java on Airflow demo

The code in this repo is used to showcase how you can package up Java code in a container image, and then run this via an Airflow Operator. To demostrate this we need some demo code that does something, in this case we run a SQL query against a MySQL database, and then store the output of that as a CSV file in an Amazon S3 bucket. Pretty typical stuff, and enough to show you how the key pieces work.

**Building the Java on Airflow Container**

You can build the container by running the following command from the java-on-airflow directory

```
docker build -t java-on-airflow .
```
Which should generate output similar to the following

```
[+] Building 38.8s (11/11) FINISHED                                                                                                                                             docker:desktop-linux
 => [internal] load .dockerignore                                                                                                                                                               0.0s
 => => transferring context: 2B                                                                                                                                                                 0.0s
 => [internal] load build definition from Dockerfile                                                                                                                                            0.0s
 => => transferring dockerfile: 302B                                                                                                                                                            0.0s
 => [internal] load metadata for docker.io/library/amazoncorretto:17                                                                                                                            1.1s
 => [internal] load build context                                                                                                                                                               0.0s
 => => transferring context: 972B                                                                                                                                                               0.0s
 => CACHED [builder 1/5] FROM docker.io/library/amazoncorretto:17@sha256:eaa4ff4026b888b602b9cef6875a7b763ab4b3076f1257c14237bd31bea54167                                                       0.0s
 => [builder 2/5] COPY . /app                                                                                                                                                                   0.0s
 => [builder 3/5] COPY app /app                                                                                                                                                                 0.0s
 => [builder 4/5] WORKDIR /app                                                                                                                                                                  0.0s
 => [builder 5/5] RUN ./mvnw package                                                                                                                                                           37.3s
 => [stage-1 2/2] COPY --from=builder /app/target/airflow-java-1.0-SNAPSHOT.jar /app/                                                                                                           0.1s 
 => exporting to image                                                                                                                                                                          0.1s 
 => => exporting layers                                                                                                                                                                         0.1s 
 => => writing image sha256:e46474122a4abeae9d0b43d21add1aaa75aaddf595f074d4a30c20925df2394e                                                                                                    0.0s 
 => => naming to docker.io/library/java-on-airflow                                                                                                                                                  0.0s 
                                                     
```

You can now run the Java script using the following command

```
docker run  java-on-airflow
```
Which should ouput the following:
```
Usage: java DatabaseToS3Exporter <db-server> <db-name> <sql-query> <s3-bucket-name> <aws-region> <secret-arn>
```

**Uploading to the container image repository**

I have provided a simple script that automates the building and pushing of this container image to a container image repository running on Amazon ECR. To run, first edit the setup.sh file in the java-on-airflow directory (you will need to update your AWS account details, AWS region, etc - its pretty simple) and then you can simply use the following command from the command line to run everything

```
./setup.sh
```

you should get something similar to this

```
Login Succeeded

An error occurred (RepositoryNotFoundException) when calling the DescribeRepositories operation: The repository with name 'ato-airflow' does not exist in the registry with id '704533066374'
Creating repos as it does not exists
[+] Building 32.0s (12/12) FINISHED                                                                                                                                             docker:desktop-linux
 => [internal] load .dockerignore                                                                                                                                                               0.0s
 => => transferring context: 2B                                                                                                                                                                 0.0s
 => [internal] load build definition from Dockerfile                                                                                                                                            0.0s
 => => transferring dockerfile: 290B                                                                                                                                                            0.0s
 => [internal] load metadata for docker.io/library/amazoncorretto:17                                                                                                                            0.9s
 => [auth] library/amazoncorretto:pull token for registry-1.docker.io                                                                                                                           0.0s
 => [internal] load build context                                                                                                                                                               0.0s
 => => transferring context: 960B                                                                                                                                                               0.0s
 => CACHED [builder 1/5] FROM docker.io/library/amazoncorretto:17@sha256:eaa4ff4026b888b602b9cef6875a7b763ab4b3076f1257c14237bd31bea54167                                                       0.0s
 => [builder 2/5] COPY . /app                                                                                                                                                                   0.0s
 => [builder 3/5] COPY app /app                                                                                                                                                                 0.0s
 => [builder 4/5] WORKDIR /app                                                                                                                                                                  0.0s
 => [builder 5/5] RUN ./mvnw package                                                                                                                                                           30.7s
 => [stage-1 2/2] COPY --from=builder /app/target/airflow-java-1.0-SNAPSHOT.jar /app/                                                                                                           0.0s 
 => exporting to image                                                                                                                                                                          0.1s 
 => => exporting layers                                                                                                                                                                         0.1s 
 => => writing image sha256:97a3535a34a765d8986e371b61edb26aeb8ba9858281de4648946531562375d2                                                                                                    0.0s 
 => => naming to xxxx.dkr.ecr.eu-west-1.amazonaws.com/ato-airflow:latest                                                                                                                0.0s 
                                                                                                                                                                                                     
What's Next?
  View a summary of image vulnerabilities and recommendations → docker scout quickview
The push refers to repository [704533066374.dkr.ecr.eu-west-1.amazonaws.com/ato-airflow]
82fba2b5455b: Pushed 
e10e452b681d: Pushed 
4f9883c58bf0: Pushed 
airflw-amd64: digest: sha256:29ab4687c9f3e881d08bfeea57f115fe21668e531ecd1c64b5967b629ed865a2 size: 954
Created manifest list xxxx.dkr.ecr.eu-west-1.amazonaws.com/ato-airflow:airflw
{
   "schemaVersion": 2,
   "mediaType": "application/vnd.docker.distribution.manifest.list.v2+json",
   "manifests": [
      {
         "mediaType": "application/vnd.docker.distribution.manifest.v2+json",
         "size": 954,
         "digest": "sha256:29ab4687c9f3e881d08bfeea57f115fe21668e531ecd1c64b5967b629ed865a2",
         "platform": {
            "architecture": "amd64",
            "os": "linux"
         }
      }
   ]
}
sha256:0ed51cc743aff6491265ef190fff46423b4c7fddb53e9ddc310d555ed49ca296
```


**Local Setup**

You can run/test locally, although the script does use AWS to 1/grab secrets information to connect to the MySQL database, 2/upload the query in csv format. You could change the Java code to do this differently if you wanted.

To run this against a local MySQL instance, I used the following to first start a local MySQL test instance.

```
docker run --name mysql -d \
    -p 3306:3306 \
    -e MYSQL_ROOT_PASSWORD=change-me \
    --restart unless-stopped \
    mysql:8
````
I then updated the username/password in the AWS Secrets Manager.
