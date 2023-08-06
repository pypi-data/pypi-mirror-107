Pytest plugin for Test IT
==========================
.. image:: https://img.shields.io/pypi/v/testit-pytest?style=plastic
        :target: https://pypi.org/project/testit-pytest/

.. image:: https://img.shields.io/pypi/dm/testit-pytest?style=plastic
        :target: https://pypi.org/project/testit-pytest/

.. image:: https://img.shields.io/pypi/pyversions/testit-pytest?style=plastic
        :target: https://pypi.org/project/testit-pytest/

Installation
=============

.. code:: bash

    $ pip install testit-pytest

Simple connection_config.ini
=============================

You need to put the connection_config.ini file in the root directory of the project.

.. code:: ini

    [testit]
    url = https://{DOMAIN} - location of the Test IT instance
    privatetoken = it has the form {T2lKd2pLZGI4WHRhaVZUejNl}
        1. go to the http://{DOMAIN}/user-profile profile
        2. copy the API secret key
    projectID = it has the form {5236eb3f-7c05-46f9-a609-dc0278896464}
        1. create a project
        2. open DevTools -> network
        3. go to the project http://{DOMAIN}/projects/20/tests
        4. GET-request project, Preview tab, copy id field
    configurationID = it has the form {15dbb164-c1aa-4cbf-830c-8c01ae14f4fb}
        1. create a project
        2. open DevTools -> network
        3. go to the project http://{DOMAIN}/projects/20/tests
        4. GET-request configurations, Preview tab, copy id field

Usage
======

.. code:: bash

    $ pytest --testit

Simple tests
=============

.. code:: py

    import pytest
    import testit

    @testit.workItemID(627)
    @testit.displayName('Simple autotest 1 - {name}')
    @testit.externalID('Simple_autotest1_{name}')
    @testit.title('Authorization')
    @testit.description('E2E_autotest')
    @testit.labels('{labels}')
    @testit.link(url='https://roviti2348.atlassian.net/browse/JCP-15593')
    @testit.link(url='{url}', type='{link_type}', title='{link_title}')
    @pytest.mark.parametrize('name, labels, url, link_type, link_title', [
        ('param 1', ['E2E', 'test'], 'https://dumps.example.com/module/JCP-15593', testit.LinkType.DEFECT, 'JCP-15593'),
        ('param 2', (), 'https://github.com/testit-tms/listener-csharp', testit.LinkType.RELATED, 'Listener'),
        ('param 3', ('E2E', 'test'), 'https://best-tms.testit.software/projects', testit.LinkType.REQUIREMENT, ''),
        ('param 4', {'E2E', 'test'}, 'https://testit.software/', testit.LinkType.BLOCKED_BY, 'Test IT'),
        ('param 5', 'test', 'https://github.com/testit-tms', testit.LinkType.REPOSITORY, 'GitHub')
    ])
    def test_1(self, name, labels, url, link_type, link_title):
        testit.addLink(title='component_dump.dmp', type=testit.LinkType.RELATED, url='https://dumps.example.com/module/some_module_dump')
        testit.addLink(title='component_dump.dmp', type=testit.LinkType.BLOCKED_BY, url='https://dumps.example.com/module/some_module_dump')
        testit.addLink(title='component_dump.dmp', type=testit.LinkType.DEFECT, url='https://dumps.example.com/module/some_module_dump')
        testit.addLink(title='component_dump.dmp', type=testit.LinkType.ISSUE, url='https://dumps.example.com/module/some_module_dump')
        testit.addLink(title='component_dump.dmp', type=testit.LinkType.REQUIREMENT, url='https://dumps.example.com/module/some_module_dump')
        testit.addLink(title='component_dump.dmp', type=testit.LinkType.REPOSITORY, url='https://dumps.example.com/module/some_module_dump')
        with testit.step('Log in the system', 'system authentication'):
            with testit.step('Enter the login', 'login was entered'):
                with testit.step('Enter the password', 'password was entered'):
                    assert True
            with testit.step('Create a project', 'the project was created'):
                with testit.step('Enter the project', 'the contents of the project are displayed'):
                    assert True
                with testit.step('Create a test case', 'test case was created'):
                    assert True
        with testit.step('Attachments'):
            testit.attachments(join(dirname(__file__), 'docs/text_file.txt'), join(dirname(__file__), 'pictures/picture.jpg'), join(dirname(__file__), 'docs/document.docx'))
            testit.attachments(join(dirname(__file__), 'docs/document.doc'), join(dirname(__file__), 'docs/logs.log'))
            assert True
        with testit.step('step 3'):
            assert True
        with testit.step('step 4'):
            assert True

    @testit.externalID('Simple_autotest2')
    def test_2():
        """Simple autotest 2"""
        assert oneStep()
        assert two_step()

    @testit.step
    def oneStep():
        assert oneOneStep()
        assert oneTwoStep()
        return True

    @testit.step
    def twoStep():
        return True

    @testit.step('step 1.1', 'description')
    def oneOneStep():
        return True

    @testit.step('step 2')
    def oneTwoStep():
        return True

    @testit.externalID('Simple_test_skip')
    @testit.displayName('Simple test skip')
    @pytest.mark.skipif(True, reason='Because i can')
    def test_skip():
        assert True
