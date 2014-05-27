#
# Making the VNC applet.
#

CP = cp
RM = rm
JC = javac
JAR = jar
ARCHIVE = SboxPlayer.jar
MANIFEST = MANIFEST.MF
PAGES = index.html
INSTALL_DIR = ./classes

CLASSES = RfbPlayer.class RfbProto.class ButtonPanel.class VncCanvas.class \
	  FbsInputStream.class FbsEntryPoint.class \
	  LWScrollPane.class \
	  PARfbSender.class RfbPlayerSetDisplaySize.class \
	  FbsConnection.class  RfbSharedStatic.class

SOURCES = RfbPlayer.java RfbProto.java ButtonPanel.java VncCanvas.java \
	  FbsInputStream.java FbsEntryPoint.java LWScrollPane.java \
	  PARfbSender.java RfbPlayerSetDisplaySize.java \
	  FbsConnection.java RfbSharedStatic.java

all: $(CLASSES) $(ARCHIVE)

$(CLASSES): $(SOURCES)
	$(JC) -g $(SOURCES)

$(ARCHIVE): $(CLASSES) $(MANIFEST) $(PAGES)
	$(JAR) cfm $(ARCHIVE) $(MANIFEST) *.class $(PAGES)

install: $(CLASSES) $(ARCHIVE)
	$(CP) *.class $(ARCHIVE) $(PAGES) $(INSTALL_DIR)

clean::
	$(RM) *.class *.jar
