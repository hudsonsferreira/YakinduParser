package org.yakindu.sct.ui.editor.factories;

import org.eclipse.draw2d.ColorConstants;
import org.eclipse.emf.ecore.resource.Resource;
import org.eclipse.gmf.runtime.diagram.core.preferences.PreferencesHint;
import org.eclipse.gmf.runtime.diagram.core.services.ViewService;
import org.eclipse.gmf.runtime.diagram.core.util.ViewUtil;
import org.eclipse.gmf.runtime.draw2d.ui.figures.FigureUtilities;
import org.eclipse.gmf.runtime.notation.Bounds;
import org.eclipse.gmf.runtime.notation.DecorationNode;
import org.eclipse.gmf.runtime.notation.Diagram;
import org.eclipse.gmf.runtime.notation.Node;
import org.eclipse.gmf.runtime.notation.NotationFactory;
import org.eclipse.gmf.runtime.notation.ShapeStyle;
import org.eclipse.gmf.runtime.notation.View;
import org.yakindu.sct.model.sgraph.Entry;
import org.yakindu.sct.model.sgraph.EntryKind;
import org.yakindu.sct.model.sgraph.Region;
import org.yakindu.sct.model.sgraph.SGraphFactory;
import org.yakindu.sct.model.sgraph.State;
import org.yakindu.sct.model.sgraph.Statechart;
import org.yakindu.sct.model.sgraph.Transition;
import org.yakindu.sct.ui.editor.DiagramActivator;
import org.yakindu.sct.ui.editor.editor.StatechartDiagramEditor;
import org.yakindu.sct.ui.editor.providers.SemanticHints;

public final class FactoryUtils {

    private static final int INITIAL_REGION_WIDTH = 600;
    private static final int INITIAL_REGION_HEIGHT = 400;
    private static final String INITIAL_REGION_NAME = "main region";

    private static final int INITIAL_TEXT_COMPARTMENT_X = 10;
    private static final int INITIAL_TEXT_COMPARTMENT_Y = 10;
    private static final int INITIAL_TEXT_COMPARTMENT_HEIGHT = 400;
    private static final int INITIAL_TEXT_COMPARTMENT_WIDTH = 200;

    private static final int SPACING = 10;

    private FactoryUtils() {
    }

    @SuppressWarnings("unchecked")
    public static Node createLabel(View owner, String hint) {
        DecorationNode nameLabel = NotationFactory.eINSTANCE
                .createDecorationNode();
        nameLabel.setType(hint);

        ShapeStyle style = NotationFactory.eINSTANCE.createShapeStyle();
        style.setFontColor(FigureUtilities.RGBToInteger(ColorConstants.black
                .getRGB()));
        nameLabel.getStyles().add(style);

        ViewUtil.insertChildView(owner, nameLabel, ViewUtil.APPEND, true);
        nameLabel.setLayoutConstraint(NotationFactory.eINSTANCE
                .createLocation());
        return nameLabel;
    }

    public static void createStatechartModel(Resource resource) {
        createStatechartModel(resource,
                DiagramActivator.DIAGRAM_PREFERENCES_HINT);
    }

    public static void createStatechartModel(Resource resource,
            PreferencesHint preferencesHint) {
        Statechart statechart = SGraphFactory.eINSTANCE.createStatechart();
        statechart.setSpecification("\n\ninterface light:\nvar off:boolean\nvar on:boolean\n\ninterface thermostat:\nvar minimum:boolean\nvar maximum:boolean\n\ninterface:\nin event opendoor\nin event closedoor");

        String lastSegment = resource.getURI().lastSegment();
        String statechartName = lastSegment.substring(0,
                lastSegment.indexOf('.'));
        statechart.setName(statechartName);

        Diagram diagram = ViewService.createDiagram(statechart,
                StatechartDiagramEditor.ID, preferencesHint);
        diagram.setElement(statechart);

        resource.getContents().add(statechart);
        resource.getContents().add(diagram);

        Region region = SGraphFactory.eINSTANCE.createRegion();
        region.setName(INITIAL_REGION_NAME);
        statechart.getRegions().add(region);
        Node regionView = ViewService.createNode(diagram, region,
                SemanticHints.REGION, preferencesHint);
        setRegionViewLayoutConstraint(regionView);

        Entry initialState = SGraphFactory.eINSTANCE.createEntry();
        initialState.setKind(EntryKind.INITIAL);
        region.getVertices().add(initialState);
        Node initialStateView = ViewService.createNode(
                getRegionCompartmentView(regionView), initialState,
                SemanticHints.ENTRY, preferencesHint);
        setInitialStateViewLayoutConstraint(initialStateView);
        
        
        State refrigeratordoorclosed = SGraphFactory.eINSTANCE.createState();
        refrigeratordoorclosed.setName("refrigeratordoorclosed"); 
        refrigeratordoorclosed.setSpecification("entry/\nlight.off = true;\nlight.on = false;\nthermostat.minimum = true;\nthermostat.maximum = false"); 
        region.getVertices().add(refrigeratordoorclosed); 
        Node refrigeratordoorclosedNode = ViewService.createNode(
        getRegionCompartmentView(regionView), refrigeratordoorclosed,
        SemanticHints.STATE, preferencesHint);
        setStateViewLayoutConstraintrefrigeratordoorclosed(refrigeratordoorclosedNode);

        State refrigeratordooropened = SGraphFactory.eINSTANCE.createState();
        refrigeratordooropened.setName("refrigeratordooropened"); 
        refrigeratordooropened.setSpecification("entry/\nlight.on = true;\nlight.off = false;\nthermostat.maximum = true;\nthermostat.minimum = false"); 
        region.getVertices().add(refrigeratordooropened); 
        Node refrigeratordooropenedNode = ViewService.createNode(
        getRegionCompartmentView(regionView), refrigeratordooropened,
        SemanticHints.STATE, preferencesHint);
        setStateViewLayoutConstraintrefrigeratordooropened(refrigeratordooropenedNode);

        Transition opendoor = SGraphFactory.eINSTANCE.createTransition();
        opendoor.setSpecification("opendoor");
        opendoor.setSource(refrigeratordoorclosed);
        opendoor.setTarget(refrigeratordooropened);

        Transition closedoor = SGraphFactory.eINSTANCE.createTransition();
        closedoor.setSpecification("closedoor");
        closedoor.setSource(refrigeratordooropened);
        closedoor.setTarget(refrigeratordoorclosed);

        Transition transition = SGraphFactory.eINSTANCE.createTransition();
        transition.setSource(initialState);
        transition.setTarget(refrigeratordoorclosed);
        initialState.getOutgoingTransitions().add(transition);
        ViewService.createEdge(initialStateView, refrigeratordoorclosedNode, transition,
        SemanticHints.TRANSITION, preferencesHint);
        Node textCompartment = ViewService.createNode(diagram, statechart,
        SemanticHints.STATECHART_TEXT, preferencesHint);
        setTextCompartmentLayoutConstraint(textCompartment);
        }

    private static void setStateViewLayoutConstraintrefrigeratordoorclosed(Node refrigeratordoorclosedNode) {
    Bounds boundsrefrigeratordoorclosedNode = NotationFactory.eINSTANCE.createBounds();
    boundsrefrigeratordoorclosedNode.setX(50);
    boundsrefrigeratordoorclosedNode.setY(60);
    refrigeratordoorclosedNode.setLayoutConstraint(boundsrefrigeratordoorclosedNode);
    }

    private static void setStateViewLayoutConstraintrefrigeratordooropened(Node refrigeratordooropenedNode) {
    Bounds boundsrefrigeratordooropenedNode = NotationFactory.eINSTANCE.createBounds();
    boundsrefrigeratordooropenedNode.setX(350);
    boundsrefrigeratordooropenedNode.setY(60);
    refrigeratordooropenedNode.setLayoutConstraint(boundsrefrigeratordooropenedNode);
    }


    private static void setInitialStateViewLayoutConstraint(
            Node initialStateView) {
        Bounds bounds = NotationFactory.eINSTANCE.createBounds();
        bounds.setX(100);
        bounds.setY(20);
        initialStateView.setLayoutConstraint(bounds);
    }

    private static View getRegionCompartmentView(View regionView) {
        return (View) regionView.getChildren().get(1);
    }

    private static void setTextCompartmentLayoutConstraint(Node textCompartment) {
        Bounds bounds = NotationFactory.eINSTANCE.createBounds();
        bounds.setX(INITIAL_TEXT_COMPARTMENT_X);
        bounds.setY(INITIAL_TEXT_COMPARTMENT_Y);
        bounds.setHeight(INITIAL_TEXT_COMPARTMENT_HEIGHT);
        bounds.setWidth(INITIAL_TEXT_COMPARTMENT_WIDTH);
        textCompartment.setLayoutConstraint(bounds);
    }

    private static void setRegionViewLayoutConstraint(Node regionView) {
        Bounds bounds = NotationFactory.eINSTANCE.createBounds();
        bounds.setX(INITIAL_TEXT_COMPARTMENT_WIDTH + INITIAL_TEXT_COMPARTMENT_X
                + SPACING);
        bounds.setY(INITIAL_TEXT_COMPARTMENT_Y);
        bounds.setHeight(INITIAL_REGION_HEIGHT);
        bounds.setWidth(INITIAL_REGION_WIDTH);
        regionView.setLayoutConstraint(bounds);
    }
}
