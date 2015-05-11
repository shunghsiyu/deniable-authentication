# ./gen/diffiehellman_containerxml.py
# -*- coding: utf-8 -*-
# PyXB bindings for NM:e92452c8d3e28a9e27abfc9994d2007779e7f4c9
# Generated 2015-05-11 13:06:23.708024 by PyXB version 1.2.4 using Python 2.7.9.final.0
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
_GenerationUID = pyxb.utils.utility.UniqueIdentifier('urn:uuid:0d6c2726-f800-11e4-9612-3c15c2e0da90')

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
    _XSDLocation = pyxb.utils.utility.Location('/Users/shunghsiyu/git/deniable-authentication/diffiehellman_container.xsd', 3, 6)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element a uses Python identifier a
    __a = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'a'), 'a', '__AbsentNamespace0_CTD_ANON_a', False, pyxb.utils.utility.Location('/Users/shunghsiyu/git/deniable-authentication/diffiehellman_container.xsd', 5, 14), )

    
    a = property(__a.value, __a.set, None, None)

    
    # Element r uses Python identifier r
    __r = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'r'), 'r', '__AbsentNamespace0_CTD_ANON_r', False, pyxb.utils.utility.Location('/Users/shunghsiyu/git/deniable-authentication/diffiehellman_container.xsd', 6, 14), )

    
    r = property(__r.value, __r.set, None, None)

    
    # Element k uses Python identifier k
    __k = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'k'), 'k', '__AbsentNamespace0_CTD_ANON_k', False, pyxb.utils.utility.Location('/Users/shunghsiyu/git/deniable-authentication/diffiehellman_container.xsd', 7, 14), )

    
    k = property(__k.value, __k.set, None, None)

    
    # Element data uses Python identifier data
    __data = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'data'), 'data', '__AbsentNamespace0_CTD_ANON_data', False, pyxb.utils.utility.Location('/Users/shunghsiyu/git/deniable-authentication/diffiehellman_container.xsd', 8, 14), )

    
    data = property(__data.value, __data.set, None, None)

    _ElementMap.update({
        __a.name() : __a,
        __r.name() : __r,
        __k.name() : __k,
        __data.name() : __data
    })
    _AttributeMap.update({
        
    })



container = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'container'), CTD_ANON, location=pyxb.utils.utility.Location('/Users/shunghsiyu/git/deniable-authentication/diffiehellman_container.xsd', 2, 2))
Namespace.addCategoryObject('elementBinding', container.name().localName(), container)



CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'a'), pyxb.binding.datatypes.string, scope=CTD_ANON, location=pyxb.utils.utility.Location('/Users/shunghsiyu/git/deniable-authentication/diffiehellman_container.xsd', 5, 14)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'r'), pyxb.binding.datatypes.base64Binary, scope=CTD_ANON, location=pyxb.utils.utility.Location('/Users/shunghsiyu/git/deniable-authentication/diffiehellman_container.xsd', 6, 14)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'k'), pyxb.binding.datatypes.base64Binary, scope=CTD_ANON, location=pyxb.utils.utility.Location('/Users/shunghsiyu/git/deniable-authentication/diffiehellman_container.xsd', 7, 14)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'data'), pyxb.binding.datatypes.base64Binary, scope=CTD_ANON, location=pyxb.utils.utility.Location('/Users/shunghsiyu/git/deniable-authentication/diffiehellman_container.xsd', 8, 14)))

def _BuildAutomaton ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton
    del _BuildAutomaton
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(None, 'a')), pyxb.utils.utility.Location('/Users/shunghsiyu/git/deniable-authentication/diffiehellman_container.xsd', 5, 14))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(None, 'r')), pyxb.utils.utility.Location('/Users/shunghsiyu/git/deniable-authentication/diffiehellman_container.xsd', 6, 14))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(None, 'k')), pyxb.utils.utility.Location('/Users/shunghsiyu/git/deniable-authentication/diffiehellman_container.xsd', 7, 14))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(None, 'data')), pyxb.utils.utility.Location('/Users/shunghsiyu/git/deniable-authentication/diffiehellman_container.xsd', 8, 14))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
         ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
         ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    st_3._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON._Automaton = _BuildAutomaton()

