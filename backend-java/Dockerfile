FROM eclipse-temurin:17-jdk
WORKDIR /app
COPY . /app
RUN ./mvnw package -DskipTests
CMD ["java", "-jar", "target/your-app.jar"]
