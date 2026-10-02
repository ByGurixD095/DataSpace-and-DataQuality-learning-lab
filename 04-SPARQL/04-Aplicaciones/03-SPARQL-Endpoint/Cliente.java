import java.net.URI;
import java.net.URLEncoder;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.nio.charset.StandardCharsets;

/**
 * Cliente de un endpoint SPARQL con java.net.http (solo JDK 11+, sin dependencias).
 *
 *   java Cliente.java                                  → contra servidor.py
 *   java Cliente.java http://localhost:3030/ds/sparql  → contra otro endpoint (p. ej. Fuseki)
 */
public class Cliente {

    public static void main(String[] args) throws Exception {
        String endpoint = args.length > 0 ? args[0] : "http://localhost:3030/sparql";

        String consulta = """
            PREFIX ex: <http://example.org/>
            SELECT ?nombre ?edad
            WHERE { ?p a ex:Persona ; ex:nombre ?nombre ; ex:edad ?edad . }
            ORDER BY DESC(?edad) LIMIT 3
            """;

        System.out.println("— JSON —");
        System.out.println(consultar(endpoint, consulta, "application/sparql-results+json"));

        System.out.println("— CSV —");
        System.out.println(consultar(endpoint, consulta, "text/csv"));
    }

    static String consultar(String endpoint, String consulta, String accept) throws Exception {
        String cuerpo = "query=" + URLEncoder.encode(consulta, StandardCharsets.UTF_8);

        HttpRequest peticion = HttpRequest.newBuilder(URI.create(endpoint))
                .header("Content-Type", "application/x-www-form-urlencoded")
                .header("Accept", accept)
                .POST(HttpRequest.BodyPublishers.ofString(cuerpo))
                .build();

        HttpResponse<String> respuesta = HttpClient.newHttpClient()
                .send(peticion, HttpResponse.BodyHandlers.ofString());

        if (respuesta.statusCode() != 200) {
            throw new RuntimeException("HTTP " + respuesta.statusCode() + ": " + respuesta.body());
        }
        return respuesta.body();
    }
}
