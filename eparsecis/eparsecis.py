# -*- coding: utf-8 -*-

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Copyright 2018 SerialLab, LLC.  All rights reserved.

from lxml import etree
import logging

from EPCPyYes.core.v1_2 import template_events
from EPCPyYes.core.v1_2.events import Action, BusinessTransaction
from EPCPyYes.core.v1_2.events import Source, Destination, QuantityElement
from EPCPyYes.core.v1_2.CBV.helpers import get_ilmd_enum_by_value
from EPCPyYes.core.v1_2.CBV.instance_lot_master_data import \
    InstanceLotMasterDataAttribute

from eparsecis.elements import EPCPyYesElement

logger = logging.getLogger()


class EPCISParser(object):
    '''
    Parses EPCIS XML from a stream and serializes each EPCIS Event
    in a given document into a serialized EPCPyYes event object.
    '''

    def __init__(self, stream):
        '''
        Initialize a new EPCISParser with a stream to be
        parsed.
        :param stream: The stream containing the EPCIS XML to be parsed.
        '''
        self._stream = stream

    @property
    def stream(self):
        return self._stream

    @stream.setter
    def stream(self, value):
        self._stream = value

    def parse(self):
        parser_lookup = etree.ElementDefaultClassLookup(
            element=EPCPyYesElement)
        epcis = etree.iterparse(self.stream, events=('start', 'end'))
        epcis.set_element_class_lookup(parser_lookup)
        for event, element in epcis:
            if element.tag == 'ObjectEvent':
                self.parse_object_event_element(event, element)
            elif element.tag == 'AggregationEvent':
                self.parse_aggregation_event_element(event, element)
            elif element.tag == 'TransactionEvent':
                self.parse_transaction_event_element(event, element)
            elif element.tag == 'TransformationEvent':
                self.parse_transformation_event_element(event, element)

    def parse_object_event_element(self, event, object_element):
        oevent = None
        logger.debug('handling object event')
        if event == 'start':
            oevent = template_events.ObjectEvent(epc_list=[], quantity_list=[])
            for child in object_element:
                logger.debug('%s,%s', child.tag, child.text.strip())
                if child.tag == 'eventTime':
                    oevent.event_time = child.text.strip()
                elif child.tag == 'bizTransactionList':
                    self.parse_biz_transaction_list(oevent, child)
                elif child.tag == 'eventTimeZoneOffset':
                    oevent.event_timezone_offset = child.text.strip()
                elif child.tag == 'recordTime':
                    oevent.record_time = child.text.strip()
                elif child.tag == 'epcList':
                    self.parse_epc_list(oevent, child)
                elif child.tag == 'action':
                    oevent.action = Action(child.text.strip())
                elif child.tag == 'bizStep':
                    oevent.biz_step = child.text.strip()
                elif child.tag == 'disposition':
                    oevent.disposition = child.text.strip()
                elif child.tag == 'readPoint':
                    self.parse_readpoint(oevent, child)
                elif child.tag == 'bizLocation':
                    self.parse_biz_location(oevent, child)
                elif child.tag == 'extension':
                    self.parse_extension(oevent, child)
        elif event == 'end':
            logger.debug('clearing out the Element')
            object_element.clear()
        if oevent:
            self.handle_object_event(oevent)

    def parse_aggregation_event_element(self, event, aggregation_element):
        aevent = None
        logger.debug('handling aggregation event')
        if event == 'start':
            aevent = template_events.AggregationEvent()
            for child in aggregation_element:
                logger.debug('%s,%s', child.tag, child.text.strip())
                if child.tag == 'eventTime':
                    aevent.event_time = child.text.strip().strip()
                elif child.tag == 'eventTimeZoneOffset':
                    aevent.event_timezone_offset = child.text.strip()
                elif child.tag == 'bizTransactionList':
                    self.parse_biz_transaction_list(aevent, child)
                elif child.tag == 'recordTime':
                    aevent.record_time = child.text.strip().strip()
                elif child.tag == 'parentID':
                    aevent.parent_id = child.text.strip().strip()
                elif child.tag == 'childEPCs':
                    self.parse_epc_list(aevent, child)
                elif child.tag == 'action':
                    aevent.action = Action(child.text.strip().strip())
                elif child.tag == 'bizStep':
                    aevent.biz_step = child.text.strip().strip()
                elif child.tag == 'disposition':
                    aevent.disposition = child.text.strip().strip()
                elif child.tag == 'readPoint':
                    self.parse_readpoint(aevent, child)
                elif child.tag == 'bizLocation':
                    self.parse_biz_location(aevent, child)
                elif child.tag == 'extension':
                    self.parse_extension(aevent, child)
        elif event == 'end':
            logger.debug('clearing out the Element')
            aggregation_element.clear()
        if aevent:
            self.handle_aggregation_event(aevent)

    def parse_transaction_event_element(self, event, transaction_element):
        tevent = None
        logger.debug('handling transaction event')
        if event == 'start':
            tevent = template_events.TransactionEvent()
            for child in transaction_element:
                logger.debug('%s,%s', child.tag, child.text.strip())
                if child.tag == 'eventTime':
                    tevent.event_time = child.text.strip()
                elif child.tag == 'bizTransactionList':
                    self.parse_biz_transaction_list(tevent, child)
                elif child.tag == 'eventTimeZoneOffset':
                    tevent.event_timezone_offset = child.text.strip()
                elif child.tag == 'recordTime':
                    tevent.record_time = child.text.strip()
                elif child.tag == 'parentID':
                    tevent.parent_id = child.text.strip()
                elif child.tag == 'epcList':
                    self.parse_epc_list(tevent, child)
                elif child.tag == 'action':
                    tevent.action = Action(child.text.strip())
                elif child.tag == 'bizStep':
                    tevent.biz_step = child.text.strip()
                elif child.tag == 'disposition':
                    tevent.disposition = child.text.strip()
                elif child.tag == 'readPoint':
                    self.parse_readpoint(tevent, child)
                elif child.tag == 'bizLocation':
                    self.parse_biz_location(tevent, child)
                elif child.tag == 'extension':
                    self.parse_extension(tevent, child)
        elif event == 'end':
            logger.debug('clearing out the Element')
            transaction_element.clear()
        if tevent:
            self.handle_transaction_event(tevent)

    def parse_transformation_event_element(
        self,
        event,
        transformation_element
    ):
        tevent = None
        logger.debug('handling transaction event')
        if event == 'start':
            tevent = template_events.TransformationEvent()
            for child in transformation_element:
                if child.tag == 'eventTime':
                    tevent.event_time = child.text.strip()
                elif child.tag == 'eventTimeZoneOffset':
                    tevent.event_timezone_offset = child.text.strip()
                elif child.tag == 'recordTime':
                    tevent.record_time = child.text.strip()
                elif child.tag == 'bizTransactionList':
                    self.parse_biz_transaction_list(tevent, child)
                elif child.tag == 'eventTimeZoneOffset':
                    tevent.event_timezone_offset = child.text.strip()
                elif child.tag == 'inputEPCList':
                    self.parse_input_epc_list(tevent, child)
                elif child.tag == 'outputEPCList':
                    self.parse_output_epc_list(tevent, child)
                elif child.tag == 'transformationID':
                    tevent.transformation_id = child.text.strip()
                elif child.tag == 'bizStep':
                    tevent.biz_step = child.text.strip()
                elif child.tag == 'disposition':
                    tevent.disposition = child.text.strip()
                elif child.tag == 'readPoint':
                    self.parse_readpoint(tevent, child)
                elif child.tag == 'bizLocation':
                    self.parse_biz_location(tevent, child)
                elif child.tag == 'inputQuantityList':
                    self.parse_input_quantity_list(tevent, child)
                elif child.tag == 'outputQuantityList':
                    self.parse_output_quantity_list(tevent, child)
                elif child.tag == 'ilmd':
                    self.parse_ilmd(tevent, child)
                elif child.tag == 'sourceList':
                    self.parse_source_list(tevent, child)
                elif child.tag == 'destinationList':
                    self.parse_destination_list(tevent, child)
        elif event == 'end':
            logger.debug('clearing out the Element')
            transformation_element.clear()
        if tevent:
            self.handle_transformation_event(tevent)

    def parse_biz_transaction_list(self, event, list):
        '''
        Parses the business transaction list if supplied in a
        given event and adds that info to the event.
        :param event: The EPCIS event
        :param list: The element containing the list.
        '''
        for child in list:
            bt = BusinessTransaction(
                child.text.strip()
            )
            for name, value in child.attrib.items():
                logger.debug('%s,%s', name, value)
                if name == 'type':
                    bt.type = value
            event.business_transaction_list.append(bt)

    def parse_epc_list(self, event, list):
        '''
        Parses the epc list clearing each epc as it finds one to conserve
        memory if the list is massive.
        :param event: The EPCIS event containing the list.
        :param list: The list itself.  Either an epcList or childEPCs.
        :return: None
        '''
        if hasattr(event, 'epc_list'):
            target = event.epc_list
        elif hasattr(event, 'child_epcs'):
            target = event.child_epcs
        for epc in list:
            target.append(epc.text)
            logger.debug(epc.text)
            epc.clear()

    def parse_input_epc_list(self,
                             event: template_events.TransformationEvent,
                             list):
        '''
        Parses the epc input list of a TransformationEvent
        clearing each epc as it finds one to conserve
        memory if the list is massive.
        :param event: The EPCIS event containing the list.
        :param list: The list itself.
        :return: None
        '''
        for epc in list:
            event.input_epc_list.append(epc.text)
            logger.debug(epc.text)
            epc.clear()

    def parse_output_epc_list(self,
                              event: template_events.TransformationEvent,
                              list):
        '''
        Parses the epc output list of a TransformationEvent
        clearing each epc as it finds one to conserve
        memory if the list is massive.
        :param event: The EPCIS event containing the list.
        :param list: The list itself.
        :return: None
        '''
        for epc in list:
            event.output_epc_list.append(epc.text)
            logger.debug(epc.text)
            epc.clear()

    def parse_readpoint(self, epcis_event, read_point):
        for child in read_point:
            if child.tag == 'id':
                epcis_event.read_point = child.text.strip()
                logger.debug('%s,%s', child.tag, child.text.strip())

    def parse_biz_location(self, epcis_event, biz_location):
        for child in biz_location:
            if child.tag == 'id':
                epcis_event.biz_location = child.text.strip()
                logger.debug('%s,%s', child.tag, child.text.strip())

    def parse_extension(self, epcis_event, extension):
        '''
        Called when the extension is encountered for each event.
        If you need to process custom extensions, override this function.
        :param epcis_event: The inbound event
        :param extension: The extension lxml element.
        :return: None
        '''
        # Transformation events don't have standardized extensions...
        if not isinstance(epcis_event, template_events.TransformationEvent):
            for child in extension:
                if child.tag == 'sourceList':
                    self.parse_source_list(epcis_event, child)
                elif child.tag == 'destinationList':
                    self.parse_destination_list(epcis_event, child)
                elif child.tag == 'ilmd':
                    self.parse_ilmd(epcis_event, child)
                elif child.tag == 'quantityList':
                    self.parse_quantity_list(epcis_event, child)
                elif child.tag == 'childQuantityList':
                    self.parse_child_quantity_list(epcis_event, child)

    def parse_source_list(self, epcis_event, source_list):
        for child in source_list:
            urn = None
            for name, value in child.attrib.items():
                logger.debug('%s,%s', name, value)
                if name == 'type':
                    urn = value
            logger.debug('%s,%s', child.tag, child.text.strip())
            source = Source(urn, child.text.strip())
            epcis_event.source_list.append(source)
            logger.debug('Added %s, %s to the source_list.', urn,
                         child.text.strip())

    def parse_destination_list(self, epcis_event, destination_list):
        for child in destination_list:
            urn = None
            for name, value in child.attrib.items():
                logger.debug('%s,%s', name, value)
                if name == 'type':
                    urn = value
            logger.debug('%s,%s', child.tag, child.text.strip())
            destination = Destination(urn, child.text.strip())
            epcis_event.destination_list.append(destination)
            logger.debug('Added %s, %s to the destination_list.', urn,
                         child.text.strip())

    def parse_ilmd(self, epcis_event, ilmd):
        for child in ilmd:
            logger.debug('%s,%s', child.tag, child.text.strip())
            if child.prefix == 'cbvmd':
                check_val = child.tag.split('}')[1]
                logger.debug("check_val = %s" % check_val)
                enum = get_ilmd_enum_by_value(check_val)
                ilmd = InstanceLotMasterDataAttribute(enum, child.text.strip())
                epcis_event.ilmd.append(ilmd)

    def parse_quantity_list(self, epcis_event, quantity_list):
        '''
        Takes a quantity list element as an input and parses it
        into an EPCPyYes QuantityElement instance.
        :param epcis_event: The EPCPyYes event instance that will contain
        the parsed QuantityElement instance as an attribute.
        :param quantity_list: The Element containing the quantity_list.
        :return: None
        '''
        if logger.getEffectiveLevel() == logging.DEBUG:
            logger.debug(epcis_event.render())
        for child in quantity_list:
            if child.tag == 'quantityElement':
                self.parse_quantity_element(epcis_event, child)

    def parse_child_quantity_list(self, epcis_event, quantity_list):
        '''
        Takes a child quantity list element as an input and parses it
        into an EPCPyYes QuantityElement instance.
        :param epcis_event: The EPCPyYes event instance that will contain
        the parsed QuantityElement instance as an attribute.
        :param quantity_list: The Element containing the quantity_list.
        :return: None
        '''
        if logger.getEffectiveLevel() == logging.DEBUG:
            logger.debug(epcis_event.render())
        for child in quantity_list:
            if child.tag == 'quantityElement':
                epcis_event.child_quantity_list.append(
                    self.get_quantity_element(child)
                )

    def parse_input_quantity_list(self, epcis_event,
                                  quantity_list):
        '''
        Takes a transformation event input quantity list
        element as an input and parses it
        into an EPCPyYes QuantityElement instance.
        :param epcis_event: The EPCPyYes event instance that will contain
        the parsed QuantityElement instance as an attribute.
        :param quantity_list: The Element containing the quantity_list.
        :return: None
        '''
        if logger.getEffectiveLevel() == logging.DEBUG:
            logger.debug(epcis_event.render())
        for child in quantity_list:
            if child.tag == 'quantityElement':
                epcis_event.input_quantity_list.append(
                    self.get_quantity_element(child)
                )

    def parse_output_quantity_list(self, epcis_event,
                                   quantity_list):
        '''
        Takes a transformation event input quantity list
        element as an output and parses it
        into an EPCPyYes QuantityElement instance.
        :param epcis_event: The EPCPyYes event instance that will contain
        the parsed QuantityElement instance as an attribute.
        :param quantity_list: The Element containing the quantity_list.
        :return: None
        '''
        if logger.getEffectiveLevel() == logging.DEBUG:
            logger.debug(epcis_event.render())
        for child in quantity_list:
            if child.tag == 'quantityElement':
                epcis_event.output_quantity_list.append(
                    self.get_quantity_element(child)
                )

    def get_quantity_element(self, quantity_element):
        '''
        Parses and returns a quantity element.
        :param quantity_element:
        :return: An EPCPyYes QuantityElement.
        '''
        qe = QuantityElement('')
        for child in quantity_element:
            if child.tag == 'epcClass':
                qe.epc_class = child.text.strip()
            elif child.tag == 'quantity':
                qe.quantity = float(child.text.strip())
            elif child.tag == 'uom':
                qe.uom = child.text.strip()
        return qe

    def parse_quantity_element(self, epcis_event, quantity_element):
        qe = QuantityElement('')
        for child in quantity_element:
            if child.tag == 'epcClass':
                qe.epc_class = child.text.strip()
            elif child.tag == 'quantity':
                qe.quantity = float(child.text.strip())
            elif child.tag == 'uom':
                qe.uom = child.text.strip()
        logger.debug('Appending a quantity list element.')
        epcis_event.quantity_list.append(qe)

    def handle_object_event(self, epcis_event: template_events.ObjectEvent):
        '''
        Implement this method to support the handing of EPCPyYes ObjectEvent
        template class instances.
        :param epcis_event: The EPCPyYes template_events.ObjectEvent instance.
        :return: None
        '''
        if logger.getEffectiveLevel() == logging.DEBUG:
            # since render is being called here, avoiding sending to logger
            # unless debug is set
            logger.debug(epcis_event.render())
        logger.debug('handle object event called...')
        pass

    def handle_aggregation_event(
        self,
        epcis_event: template_events.AggregationEvent
    ):
        '''
        Implement this method to handle template_event.AggregationEvent
        instances as they are created during XML parsing.
        :param epcis_event: The AggregationEvent instance.
        :return: None
        '''
        if logger.getEffectiveLevel() == logging.DEBUG:
            # since render is being called here, avoiding sending to logger
            # unless debug is set
            logger.debug(epcis_event.render())
        logger.debug('handle aggregation event called...')
        pass

    def handle_transaction_event(
        self,
        epcis_event: template_events.TransactionEvent
    ):
        '''
        Implement this method to handle
        template_event.TransactionEvent instances as they are created during
        XML paring.
        :param epcis_event: The TransactionEvent instance.
        :return: None
        '''
        if logger.getEffectiveLevel() == logging.DEBUG:
            # since render is being called here, avoiding sending to logger
            # unless debug is set
            logger.debug(epcis_event.render())
        logger.debug('handle transaction event called...')
        pass

    def handle_transformation_event(
        self,
        epcis_event: template_events.TransformationEvent
    ):
        '''
        Implement this method to handle any template_event.TransformationEvent
        instaces as the are created during the parsing process.

        :param epcis_event: An EPCPyYes TransformationEvent
        :return: None
        '''
        if logger.getEffectiveLevel() == logging.DEBUG:
            # since render is being called here, avoiding sending to logger
            # unless debug is set
            logger.debug(epcis_event.render())
        logger.debug('handle transaction event called...')
        pass
