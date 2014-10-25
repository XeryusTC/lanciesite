#!/usr/bin/env python3
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lanciesite.settings")

import datetime, string, subprocess, django
from lanciesite import settings
from pubsite.models import Participant
from pointofsale.models import Account, get_current_event

if __name__ == "__main__":
	django.setup()
    os.chdir("tex")

    with open("DirectDebitForm.tex", "r") as fin:
        template = fin.read()
        form = string.Template(template)
        date = datetime.date.today().isoformat()
        e = get_current_event()

        for p in Participant.objects.filter(event=e):
            print("Generating for", p.user.get_full_name(), "...")
            try:
                a = p.account
                base_id = a.debit_id
            except:
                a = None
                base_id = 1
            data = {'name': p.user.get_full_name(), 'address': p.address, 'city': p.city, 'iban': p.iban, 'email': p.user.email}
            entryfee = {'description': e.name, 'amount': p.price, 'id': base_id*2-1, 'date': e.start_date}
            entryfee.update(data)
            if a:
                drinktab = {'description': e.name + " drinks", 'amount': "%2.2f" % (a.get_credits_used()/100), 'id': base_id*2, 'date': e.end_date}
            else:
                drinktab = {'description': "Security for drinks", 'amount': 50, 'id': base_id*2, 'date': e.end_date}
            drinktab.update(data)

            # generate the tex files
            entryfee_file = "{id}_entryfee.tex".format(id=p.pk)
            drinktab_file = "{id}_drinktab.tex".format(id=p.pk)
            with open(entryfee_file, 'w') as fout:
                fout.write(form.substitute(entryfee))
            with open(drinktab_file, 'w') as fout:
                fout.write(form.substitute(drinktab))

            # generate the pdfs
            subprocess.call(["pdflatex", "-output-directory=../static/tex", entryfee_file])
            subprocess.call(["pdflatex", "-output-directory=../static/tex", drinktab_file])
