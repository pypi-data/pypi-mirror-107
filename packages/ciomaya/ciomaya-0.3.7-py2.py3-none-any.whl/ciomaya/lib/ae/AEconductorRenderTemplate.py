"""
Entry point for the conductorRender Attribute Editor UI.

Generally, there's one attributeEditor instance for the conductorRender node type. When different nodes of that
type are selected, the same AE is shown and its contents replaced to reflect the current node.

AE templates build interfaces to each attribute in one of 2 ways:
Simple: e.g. self.addControl("preemptible")
Custom: e.g. self.callCustom(new_func, replace_func, "preemptible")

new_func builds the UI the first time the template is run. replace_func
reconfigures the template based on the current node. The purpose is efficiency -
so that the template doesn't need to rebuild everything everytime.

We call out to separate files (classes) to build each section if it uses a custom UI.
e.g. AEsoftware() is a class containing a new_func and a replace_func to manage the software
section.

"""
import pymel.core as pm
from ciomaya.lib import const as k
from ciomaya.lib.ae import (
    AEactions,
    AEdestination,
    AEemails,
    AEenvironment,
    AEextraAssets,
    AEframes,
    AEinstanceType,
    AElayers,
    AEmetadata,
    AEoutput,
    AEproject,
    AEscrapers,
    AEsoftware,
    AEtaskTemplate,
)


class AEconductorRenderTemplate(pm.ui.AETemplate):
    def __init__(self, node_name):
        """
        Define the high level arrangement of AE sections.
        """
        pm.ui.AETemplate.__init__(self, node_name)

        self.beginScrollLayout()

        self.callCustom(AEactions.create_ui, AEactions.populate_ui, "title")

        self.beginLayout("General Attributes", collapse=False)
        self.addControl("title")

        self.callCustom(AEproject.create_ui, AEproject.populate_ui, "projectName")

        self.callCustom(AElayers.create_ui, AElayers.populate_ui, "renderLayers")

        self.addSeparator()

        self.callCustom(AEinstanceType.create_ui, AEinstanceType.populate_ui, "instanceTypeName")

        self.addControl("preemptible")
        self.addSeparator()

        self.callCustom(AEdestination.create_ui, AEdestination.populate_ui, "destinationDirectory")

        self.endLayout()

        self.beginLayout("Software", collapse=False)
        self.callCustom(AEsoftware.create_ui, AEsoftware.populate_ui, "hostSoftware")
        self.endLayout()

        self.beginLayout("Frame range")
        self.addControl("chunkSize")

        self.callCustom(AEframes.create_ui, AEframes.populate_ui, "customRange")
        self.callCustom(AEframes.create_ui, AEframes.populate_ui, "scoutFrames")

        self.endLayout()

        self.beginLayout("Info", collapse=False)
        self.addControl("frameSpec")
        self.addControl("scoutSpec")
        self.addSeparator()
        self.addControl("frameCount")
        self.addControl("taskCount")
        self.addControl("scoutTaskCount")
        self.endLayout()

        self.beginLayout("Assets", collapse=False)

        self.addControl("useUploadDaemon", changeCommand=self.update_autosave_cleanup)
        self.addControl("uploadOnly")

        self.beginLayout("Asset Scrapers")
        self.callCustom(AEscrapers.create_ui, AEscrapers.populate_ui, "assetScrapers")
        self.endLayout()

        self.beginLayout("Extra Assets")
        self.callCustom(AEextraAssets.create_ui, AEextraAssets.populate_ui, "extraAssets")
        self.endLayout()

        self.endLayout()

        self.beginLayout("Notifications")
        self.callCustom(AEemails.create_ui, AEemails.populate_ui, "emailAddresses")
        self.endLayout()

        self.beginLayout("Task Command")
        # self.addControl("taskTemplate")
        self.callCustom(AEtaskTemplate.create_ui, AEtaskTemplate.populate_ui, "taskTemplate")

        self.endLayout()

        self.beginLayout("Metadata")

        self.callCustom(AEmetadata.create_ui, AEmetadata.populate_ui, "metadata")
        self.endLayout()

        self.beginLayout("Extra Environment")
        self.callCustom(AEenvironment.create_ui, AEenvironment.populate_ui, "extraEnvironment")
        self.endLayout()

        self.beginLayout("Automatic Retries")
        self.addControl("retriesWhenPreempted")
        self.addControl("retriesWhenFailed")
        self.endLayout()

        self.beginLayout("Submission Preview")
        self.addControl("doScrape", label="Display Scraped Assets")
        self.addControl("taskLimit", label="Display Tasks")
        self.callCustom(AEoutput.create_ui, AEoutput.populate_ui, "output")

        self.endLayout()

        self.beginLayout("Autosave")
        self.addControl("autosave", changeCommand=self.update_autosave_cleanup)
        self.addControl("autosaveTemplate", changeCommand=self.update_autosave_cleanup)
        self.addControl("cleanupAutosave", changeCommand=self.warn_autosave_cleanup)
        self.endLayout()

        self.beginLayout("Location")
        self.addControl("locationTag")
        self.endLayout()

        self.beginLayout("Developer")
        self.addControl("showTracebacks")
        self.addControl("fixturesDirectory")
        self.addControl("useFixtures", changeCommand=self.update_use_fixtures)
        self.endLayout()

        self.addExtraControls()

        for att in k.SUPPRESS_EXTRA_ATTS:
            self.suppress(att)

        self.endScrollLayout()

    def update_autosave_cleanup(self, nodeName):
        use_daemon = pm.PyNode(nodeName).attr("useUploadDaemon").get()
        self.dimControl(nodeName, "cleanupAutosave", use_daemon)
        do_autosave = pm.PyNode(nodeName).attr("autosave").get()
        autosave_template = pm.PyNode(nodeName).attr("autosaveTemplate").get()
        if do_autosave and autosave_template.lower().strip() == "<scene>":
            pm.PyNode(nodeName).attr("cleanupAutosave").set(False)

    def warn_autosave_cleanup(self, nodeName):
        do_autosave = pm.PyNode(nodeName).attr("autosave").get()
        do_cleanup = pm.PyNode(nodeName).attr("cleanupAutosave").get()
        autosave_template = pm.PyNode(nodeName).attr("autosaveTemplate").get()
        if do_autosave and autosave_template.lower().strip() == "<scene>" and do_cleanup:
            pm.displayWarning(
                "You are turning on cleanup autosave when the autosave template will overwrite your current scene. You probably don't want this."
            )

    def update_use_fixtures(self, nodeName):
        dim = not pm.PyNode(nodeName).attr("useFixtures").get()

        self.dimControl(nodeName, "fixturesDirectory", dim)
