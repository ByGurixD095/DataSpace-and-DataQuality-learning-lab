import org.apache.jena.query.*;
import org.apache.jena.rdf.model.Model;
import org.apache.jena.riot.RDFDataMgr;
import org.apache.jena.update.UpdateAction;

/** 02 — Dataset en memoria, SPARQL Update y CONSTRUCT con Apache Jena. */
public class ActualizarDataset {

    public static void main(String[] args) {
        // 1) Un Dataset es un conjunto de grafos: el grafo por defecto + grafos nombrados
        Dataset dataset = DatasetFactory.create();
        RDFDataMgr.read(dataset.getDefaultModel(), "../datos/personas.ttl");
        System.out.println("Triples iniciales: " + dataset.getDefaultModel().size());

        // 2) SPARQL Update
        UpdateAction.parseExecute("""
            PREFIX ex: <http://example.org/>
            INSERT DATA {
                ex:laura a ex:Persona ;
                         ex:nombre "Laura Gil" ;
                         ex:edad 25 ;
                         ex:viveEn ex:Madrid .
            }
            """, dataset);
        System.out.println("Tras INSERT DATA: " + dataset.getDefaultModel().size());

        // 3) CONSTRUCT devuelve un nuevo Model
        String construct = """
            PREFIX ex:   <http://example.org/>
            PREFIX foaf: <http://xmlns.com/foaf/0.1/>
            CONSTRUCT { ?p foaf:name ?n }
            WHERE     { ?p a ex:Persona ; ex:nombre ?n ; ex:viveEn ex:Madrid . }
            """;
        try (QueryExecution qe = QueryExecutionFactory.create(construct, dataset)) {
            Model nuevo = qe.execConstruct();
            nuevo.setNsPrefix("foaf", "http://xmlns.com/foaf/0.1/");
            System.out.println("\nPersonas de Madrid (foaf:name), en Turtle:");
            nuevo.write(System.out, "TURTLE");
        }
    }
}
