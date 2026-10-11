package lab.espacio.policy;

import org.eclipse.edc.connector.controlplane.contract.spi.policy.ContractNegotiationPolicyContext;
import org.eclipse.edc.policy.engine.spi.PolicyEngine;
import org.eclipse.edc.policy.engine.spi.RuleBindingRegistry;
import org.eclipse.edc.policy.model.Permission;
import org.eclipse.edc.runtime.metamodel.annotation.Inject;
import org.eclipse.edc.spi.system.ServiceExtension;
import org.eclipse.edc.spi.system.ServiceExtensionContext;

import static org.eclipse.edc.connector.controlplane.contract.spi.policy.ContractNegotiationPolicyContext.NEGOTIATION_SCOPE;
import static org.eclipse.edc.jsonld.spi.PropertyAndTypeNames.ODRL_USE_ACTION_ATTRIBUTE;
import static org.eclipse.edc.policy.engine.spi.PolicyEngine.ALL_SCOPES;
import static org.eclipse.edc.spi.constants.CoreConstants.EDC_NAMESPACE;

/**
 * Dos pasos para que una restricción propia tenga efecto en EDC:
 *   1) bind: decir EN QUÉ ÁMBITOS se evalúa (aquí, solo en la negociación);
 *   2) registerFunction: decir CÓMO se evalúa (la función de arriba).
 * Sin esto, el motor de políticas no sabe qué hacer con "tipoParticipante".
 *
 * Basado en PolicyFunctionsExtension de policy-01 de eclipse-edc/Samples.
 */
public class PolicyFunctionsExtension implements ServiceExtension {

    /** La clave coincide con el leftOperand de la política: EDC_NAMESPACE + "tipoParticipante". */
    static final String TIPO_PARTICIPANTE_KEY = EDC_NAMESPACE + "tipoParticipante";

    @Inject
    private RuleBindingRegistry ruleBindingRegistry;
    @Inject
    private PolicyEngine policyEngine;

    @Override
    public String name() {
        return "Laboratorio: funciones de política";
    }

    @Override
    public void initialize(ServiceExtensionContext context) {
        var monitor = context.getMonitor();

        ruleBindingRegistry.bind(ODRL_USE_ACTION_ATTRIBUTE, ALL_SCOPES);
        ruleBindingRegistry.bind(TIPO_PARTICIPANTE_KEY, NEGOTIATION_SCOPE);

        policyEngine.registerFunction(ContractNegotiationPolicyContext.class, Permission.class,
                TIPO_PARTICIPANTE_KEY, new TipoParticipanteConstraintFunction(monitor));
    }
}
