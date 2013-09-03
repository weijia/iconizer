========
Usage
========

To use iconizer in a project::

	from iconizer import Iconizer
	Iconizer().execute({"testapp_id_for_later_killing": ["d:/testapp.bat"]})
	

    
When closing iconizer, the main app will send KeyInterrupt to all processes.
Then kill processes if not terminated after several seconds.