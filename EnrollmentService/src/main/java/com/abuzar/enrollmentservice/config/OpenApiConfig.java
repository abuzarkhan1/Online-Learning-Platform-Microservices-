package com.abuzar.enrollmentservice.config;

import io.swagger.v3.oas.models.ExternalDocumentation;
import io.swagger.v3.oas.models.OpenAPI;
import io.swagger.v3.oas.models.info.Contact;
import io.swagger.v3.oas.models.info.Info;
import io.swagger.v3.oas.models.info.License;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class OpenApiConfig {

    @Bean
    public OpenAPI enrollmentOpenAPI() {
        return new OpenAPI()
                .info(new Info()
                        .title("Enrollment Service API")
                        .description("API documentation for managing course enrollments, progress tracking, and certificates.")
                        .version("v1.0.0")
                        .contact(new Contact()
                                .name("Abuzar Khan")
                                .email("abuzarkhan1242.com")
                                .url("https://abuzarkhan1.github.io/Abuzar/"))
                        .license(new License()
                                .name("Apache 2.0")
                                .url("https://www.apache.org/licenses/LICENSE-2.0")))
                .externalDocs(new ExternalDocumentation()
                        .description("Project Repository")
                        .url("https://github.com/abuzarkhan1/Online_Learning_Platform_Microservices"));
    }
}
