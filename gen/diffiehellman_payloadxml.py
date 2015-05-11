# ./gen/diffiehellman_payloadxml.py
# -*- coding: utf-8 -*-
# PyXB bindings for NM:e92452c8d3e28a9e27abfc9994d2007779e7f4c9
# Generated 2015-05-11 13:06:28.032771 by PyXB version 1.2.4 using Python 2.7.9.final.0
# Namespace AbsentNamespace0

from __future__ import unicode_literals
import pyxb
import pyxb.binding
import pyxb.binding.saxer
import io
import pyxb.utils.utility
import pyxb.utils.domutils
import sys
import pyxb.utils.six as _six

# Unique identifier for bindings created at the same time
_GenerationUID = pyxb.utils.utility.UniqueIdentifier('urn:uuid:0fffae35-f800-11e4-9906-3c15c2e0da90')

# Version of PyXB used to generate the bindings
_PyXBVersion = '1.2.4'
# Generated bindings are not compatible across PyXB versions
if pyxb.__version__ != _PyXBVersion:
    raise pyxb.PyXBVersionError(_PyXBVersion)

# Import bindings for namespaces imported into schema
import pyxb.binding.datatypes

# NOTE: All namespace declarations are reserved within the binding
Namespace = pyxb.namespace.CreateAbsentNamespace()
Namespace.configureCategories(['typeBinding', 'elementBinding'])

def CreateFromDocument (xml_text, default_namespace=None, location_base=None):
    """Parse the given XML and use the document element to create a
    Python instance.

    @param xml_text An XML document.  This should be data (Python 2
    str or Python 3 bytes), or a text (Python 2 unicode or Python 3
    str) in the L{pyxb._InputEncoding} encoding.

    @keyword default_namespace The L{pyxb.Namespace} instance to use as the
    default namespace where there is no default namespace in scope.
    If unspecified or C{None}, the namespace of the module containing
    this function will be used.

    @keyword location_base: An object to be recorded as the base of all
    L{pyxb.utils.utility.Location} instances associated with events and
    objects handled by the parser.  You might pass the URI from which
    the document was obtained.
    """

    if pyxb.XMLStyle_saxer != pyxb._XMLStyle:
        dom = pyxb.utils.domutils.StringToDOM(xml_text)
        return CreateFromDOM(dom.documentElement, default_namespace=default_namespace)
    if default_namespace is None:
        default_namespace = Namespace.fallbackNamespace()
    saxer = pyxb.binding.saxer.make_parser(fallback_namespace=default_namespace, location_base=location_base)
    handler = saxer.getContentHandler()
    xmld = xml_text
    if isinstance(xmld, _six.text_type):
        xmld = xmld.encode(pyxb._InputEncoding)
    saxer.parse(io.BytesIO(xmld))
    instance = handler.rootObject()
    return instance

def CreateFromDOM (node, default_namespace=None):
    """Create a Python instance from the given DOM node.
    The node tag must correspond to an element declaration in this module.

    @deprecated: Forcing use of DOM interface is unnecessary; use L{CreateFromDocument}."""
    if default_namespace is None:
        default_namespace = Namespace.fallbackNamespace()
    return pyxb.binding.basis.element.AnyCreateFromDOM(node, default_namespace)


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/Users/shunghsiyu/git/deniable-authentication/diffiehellman_payload.xsd', 3, 8)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element c uses Python identifier c
    __c = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'c'), 'c', '__AbsentNamespace0_CTD_ANON_c', False, pyxb.utils.utility.Location('/Users/shunghsiyu/git/deniable-authentication/diffiehellman_payload.xsd', 5, 16), )

    
    c = property(__c.value, __c.set, None, None)

    _ElementMap.update({
        __c.name() : __c
    })
    _AttributeMap.update({
        
    })



# Complex type [anonymous] with content type SIMPLE
class CTD_ANON_ (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type SIMPLE"""
    _TypeDefinition = pyxb.binding.datatypes.base64Binary
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/Users/shunghsiyu/git/deniable-authentication/diffiehellman_payload.xsd', 6, 20)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.base64Binary
    
    # Attribute csession uses Python identifier csession
    __csession = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'csession'), 'csession', '__AbsentNamespace0_CTD_ANON__csession', pyxb.binding.datatypes.base64Binary)
    __csession._DeclarationLocation = pyxb.utils.utility.Location('/Users/shunghsiyu/git/deniable-authentication/diffiehellman_payload.xsd', 9, 32)
    __csession._UseLocation = pyxb.utils.utility.Location('/Users/shunghsiyu/git/deniable-authentication/diffiehellman_payload.xsd', 9, 32)
    
    csession = property(__csession.value, __csession.set, None, None)

    
    # Attribute iv uses Python identifier iv
    __iv = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'iv'), 'iv', '__AbsentNamespace0_CTD_ANON__iv', pyxb.binding.datatypes.nonNegativeInteger)
    __iv._DeclarationLocation = pyxb.utils.utility.Location('/Users/shunghsiyu/git/deniable-authentication/diffiehellman_payload.xsd', 10, 32)
    __iv._UseLocation = pyxb.utils.utility.Location('/Users/shunghsiyu/git/deniable-authentication/diffiehellman_payload.xsd', 10, 32)
    
    iv = property(__iv.value, __iv.set, None, None)

    
    # Attribute hmac uses Python identifier hmac
    __hmac = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'hmac'), 'hmac', '__AbsentNamespace0_CTD_ANON__hmac', pyxb.binding.datatypes.base64Binary)
    __hmac._DeclarationLocation = pyxb.utils.utility.Location('/Users/shunghsiyu/git/deniable-authentication/diffiehellman_payload.xsd', 11, 32)
    __hmac._UseLocation = pyxb.utils.utility.Location('/Users/shunghsiyu/git/deniable-authentication/diffiehellman_payload.xsd', 11, 32)
    
    hmac = property(__hmac.value, __hmac.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __csession.name() : __csession,
        __iv.name() : __iv,
        __hmac.name() : __hmac
    })



payload = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'payload'), CTD_ANON, location=pyxb.utils.utility.Location('/Users/shunghsiyu/git/deniable-authentication/diffiehellman_payload.xsd', 2, 4))
Namespace.addCategoryObject('elementBinding', payload.name().localName(), payload)



CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'c'), CTD_ANON_, scope=CTD_ANON, location=pyxb.utils.utility.Location('/Users/shunghsiyu/git/deniable-authentication/diffiehellman_payload.xsd', 5, 16)))

def _BuildAutomaton ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton
    del _BuildAutomaton
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(None, 'c')), pyxb.utils.utility.Location('/Users/shunghsiyu/git/deniable-authentication/diffiehellman_payload.xsd', 5, 16))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON._Automaton = _BuildAutomaton()

