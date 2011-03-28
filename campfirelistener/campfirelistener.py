import sys
import pinder
from trac.core import *
from trac.ticket.api import ITicketChangeListener
from trac.config import Option, IntOption, ListOption, BoolOption

class CampfireListener(Component):
    implements(ITicketChangeListener)
    
    prefix = Option('campfire', 'prefix', '')
    projectPath = Option('campfire', 'path', '')
    tracfqdn = Option('campfire', 'trachost', '')
    subdomain = Option('campfire', 'subdomain', '')
    apiToken = Option('campfire', 'apitoken', '')
    roomId = Option('campfire', 'roomid', '')
    ssl = BoolOption('campfire', 'ssl', 'true')

    def _sendText(self, ticketid, text):
        try:
            c = pinder.Campfire(self.subdomain, self.apiToken, self.ssl)
            room = c.room(self.roomId)
            room.speak("%s: ticket #%i (http://%s%s/ticket/%i) %s" % (self.prefix, ticketid, self.tracfqdn, self.projectPath, ticketid, text))

        except:
            self.env.log.error("Unexpected error: %s" % (sys.exc_info()[1]))
            return

    def ticket_created(self, ticket):
        self._sendText(ticket.id, "\"%s\" created by %s. Milestone: %s" % (ticket.values['summary'][0:100], ticket.values['reporter'], ticket.values['milestone']))

    def ticket_changed(self, ticket, comment, author, old_values):
        self._sendText(ticket.id, "changed by %s, Comment: %s. Milestone: %s" % (author, comment[0:100]), ticket.values['milestone'])

    def ticket_deleted(self, ticket):
        self._sendText(ticket.id, "Ticket deleted")
