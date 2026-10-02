import org.apache.jena.query.*;
import org.apache.jena.rdf.model.Model;
import org.apache.jena.riot.RDFDataMgr;

/** 01 — Cargar un modelo RDF y ejecutar un SELECT con Apache Jena. */
public class ConsultaSelect {

    public static void main(String[] args) {
        // 1) Cargar datos RDF en un Model (grafo en memoria)
        Model modelo = RDFDataMgr.loadModel("../datos/personas.ttl");
        System.out.println("Triples cargados: " + modelo.size());

        // 2) Consulta SPARQL
        String consulta = """
            PREFIX ex: <http://example.org/>
            SELECT ?nombre ?edad
            WHERE {
                ?p a ex:Persona ; ex:nombre ?nombre ; ex:edad ?edad .
            }
            ORDER BY DESC(?edad)
            LIMIT 3
            """;

        // 3) Ejecutar y recorrer resultados (try-with-resources cierra la ejecución)
        try (QueryExecution qe = QueryExecutionFactory.create(consulta, modelo)) {
            ResultSet resultados = qe.execSelect();
            while (resultados.hasNext()) {
                QuerySolution fila = resultados.next();
                String nombre = fila.getLiteral("nombre").getString();
                int edad = fila.getLiteral("edad").getInt();
                System.out.println("  " + nombre + " — " + edad + " años");
            }
        }

        // 4) ASK: devuelve un booleano
        try (QueryExecution qe = QueryExecutionFactory.create(
                "ASK { <http://example.org/ana> <http://example.org/viveEn> <http://example.org/Madrid> }", modelo)) {
            System.out.println("¿Ana vive en Madrid? " + qe.execAsk());
        }
    }
}
