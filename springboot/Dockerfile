# Build stage
FROM maven:3.9.9-eclipse-temurin-17 AS build
WORKDIR /workspace/app

COPY pom.xml mvnw .mvn/ ./
COPY src ./src

RUN mvn -B -DskipTests package

# Runtime stage
FROM eclipse-temurin:17-jre-jammy
WORKDIR /app

COPY --from=build /workspace/app/target/demo-0.0.1-SNAPSHOT.jar /app/demo.jar

EXPOSE 8081
ENTRYPOINT ["java", "-jar", "/app/demo.jar"]
