import click
import pydoni
from .common import Verbose


@click.option('-d', '--dpath', type=click.Path(exists=True), required=True,
              help='Full path to target directory.')
@click.option('-o', '--output-fpath', type=click.Path(), default=None,
              help='If specified, write program output to this file.')
@click.option('-r', '--recursive', is_flag=True, default=False,
              help='Scan recursively and iterate down the directory tree.')
@click.option('-h', '--human-readable', is_flag=True, default=False,
              help='Display filesize in output in human-readable format')
@click.option('-p', '--progress', is_flag=True, default=False,
              help='Display progress bar while scanning directory')
@click.option('-v', '--verbose', is_flag=True, default=False,
              help='Print messages to console.')
@click.command()
def du_by_filetype(dpath, output_fpath, recursive, human_readable, progress, verbose):
    """
    List the total filesize in a directory by file type.
    """
    args, result = pydoni.__pydonicli_declare_args__(locals()), dict()

    vb = Verbose(verbose)
    filesize_dct = pydoni.du_by_filetype(dpath=dpath,
                                               recursive=recursive,
                                               human_readable=human_readable,
                                               progress=progress,
                                               verbose=verbose)

    for ftype, fsize in filesize_dct.items():
        print(f'{ftype}: {fsize}')

    if isinstance(output_fpath, str):
        with open(output_fpath, 'a') as f:
            write_lst = []
            write_lst.append(f'Directory: "{dpath}"\n')

            for ftype, fsize in filesize_dct.items():
                write_lst.append(f'{ftype}: {fsize}\n')

            f.write(''.join(write_lst).strip())

    result['result'] = filesize_dct
    pydoni.__pydonicli_register__(dict(args=args, result=result, command_name='opsys.du_by_filetype'))


@click.option('-r', '--root', type=click.Path(exists=True), required=True, multiple=True,
              help='Top-level directory to scan.')
@click.option('--recursive', is_flag=True, default=False,
              help='Scan `root` recursively and iterate down the directory tree.')
@click.option('--true-remove', is_flag=True, default=False,
              help='Delete directories that contain only empty directories.')
@click.option('--count-hidden-files/--no-count-hidden-files', is_flag=True, default=True,
              help='Count hidden files in evaluating whether directory is empty.')
@click.option('-v', '--verbose', is_flag=True, default=False,
              help='Print messages to console.')
@click.command()
def delete_empty_subdirs(root, recursive, true_remove, count_hidden_files, verbose):
    """
    Scan a directory and delete any empty bottom-level directories.
    """
    args, result = pydoni.__pydonicli_declare_args__(locals()), dict()

    dirs = list(root)
    vb = Verbose(verbose)

    removed_dirs = []
    for root in dirs:
        pydoni.delete_empty_dirs(root=root,
                                 recursive=recursive,
                                 true_remove=true_remove,
                                 count_hidden_files=count_hidden_files)
        removed_dirs += root

    if verbose:
        if len(removed_dirs):
            for dir in removed_dirs:
                vb.info('Removed: ' + dir)
        else:
            vb.info('No empty directories found', level='warn')

    result['removed_dirs'] = removed_dirs
    pydoni.__pydonicli_register__(dict(args=args, result=result, command_name='opsys.delete_empty_subdirs'))


@click.group(name='opsys')
def cli_opsys():
    """CLI tools based on operating system actions."""
    pass


cli_opsys.add_command(delete_empty_subdirs)
cli_opsys.add_command(du_by_filetype)
