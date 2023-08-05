.. highlight:: none

Subcommand sections
===================

Cloup allows to organize the subcommand of a ``Group`` (or, more in general, of
a ``MultiCommand``) in multiple help sections. Each such help section is
represented by a :class:`~cloup.Section` instance, which is just a titled
container for commands.

A ``Section`` can be:

- *sorted* -- it lists the commands in alphabetical order
- *unsorted* -- it lists the commands in the order they are added to
  the section.

All sections defined by the developer are unsorted by default. You can create a
sorted section by passing ``sorted=True`` or by using the static method
``Section.sorted()``.

You can find a runnable example that implements part of the help of Git
`here <https://github.com/janLuke/cloup/blob/master/examples/git_sections.py>`_.
The code below is based on that example.

Adding sections to a ``Group``
------------------------------

My favorite way of defining sections is doing it all in one place, just below
the ``Group`` itself, as follows:

.. tabbed:: Code
    :new-group:

    .. code-block:: python

        import cloup
        from .commands import ( # import your subcommands implemented elsewhere
            git_init, git_clone, git_rm, git_sparse_checkout, git_mv)

        @cloup.group('git')
        def git():
            return 0

        git.section(
            'Start a working area (see also: git help tutorial)',
            git_clone,
            git_init
        )

        git.section(
            'Work on the current change (see also: git help everyday)',
            git_rm,
            git_sparse_checkout,
            git_mv
        )

        # The following lines are here just to show what happens when you add
        # commands without specifying a section: they are added to a default
        # **sorted** section, which is titled "Other commands" and shown at the
        # bottom of the command help
        git.add_command(cloup.command('fake-2', help='Fake command #2')(f))
        git.add_command(cloup.command('fake-1', help='Fake command #1')(f))


.. tabbed:: Generated help

    .. code-block:: none

        Usage: git [OPTIONS] COMMAND [ARGS]...

        Options:
          --help  Show this message and exit.

        Start a working area (see also: git help tutorial):
          clone            Clone a repository into a new directory
          init             Create an empty Git repository or reinitialize an...

        Work on the current change (see also: git help everyday):
          rm               Remove files from the working tree and from the index
          sparse-checkout  Initialize and modify the sparse-checkout
          mv               Move or rename a file, a directory, or a symlink

        Other commands:
          fake-1           Fake command #1
          fake-2           Fake command #2

.. admonition:: The default section

    All commands that are not explicitly assigned to a section are assigned to a
    "default section", which is *sorted*. This section is titled "Other commands",
    unless it is the only section defined, in which case ``cloup.Group`` behaves
    like a normal ``click.Group``, naming it just "Commands".

Each call of ``section()`` creates a new ``Section`` instance and adds it to
the ``Group``. When you add a section, all the contained subcommands are of
course added to the ``Group`` (as if you called ``add_command`` for each of
them).

In alternative, you can create a list of ``Section`` objects and pass it as the
``sections`` argument of :func:`cloup.group`:

.. code-block:: python

    import cloup
    from cloup import Section

    # here, import/define commands git_init, git_clone ecc...

    SECTIONS = [
        Section('Start a working area (see also: git help tutorial)',
                git_clone, git_init),
        Section('Work on the current change (see also: git help everyday)',
                git_rm, git_sparse_checkout, git_mv)
    ]

    @cloup.group('git', sections=SECTIONS)
    def git():
        return 0


Adding a command to a ``Section``
---------------------------------
You can add subcommands one by one as you do in Click, using either:

- the decorators ``@group.command`` and ``@group.group``
- or ``group.add_command``.

In Cloup, these methods have indeed an additional (optional) argument ``section``.

.. code-block:: python

    import cloup
    from cloup import Section

    # Define sections without filling them.
    # I'm using a class as a namespace here. This is not needed.
    class Sect:
        START_WORKING_AREA = Section(
            'Start a working area (see also: git help tutorial)')
        WORK_CURRENT_CHANGE = Section(
            'Work on the current change (see also: git help everyday)'

    @cloup.group('git')
    def git():
        return 0

    @git.command('init', section=Sect.START_WORKING_AREA)
    def git_init():
        pass

    @git.command('mv', section=Sect.WORK_CURRENT_CHANGE)
    def git_mv():
        pass

Note that (differently from what happens with option groups) every time you add
a subcommand specifying a section, you are mutating the corresponding ``Section``
object.
