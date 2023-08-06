# -*- coding: utf-8 -*-
"""
Created on Wed Feb 24 23:07:46 2021

@author: hinsm
"""

import click

import objseg.runseg

@click.command(
    context_settings={'max_content_width': 120},
    name='seg'
)
@click.option(
    '-i', '--in-image',
    required=True,
    type = click.Path(exists=True, resolve_path=True),
    help = '''Path to TSV format file with copy number and allele count information for all samples.'''
    '''See the examples directory in the GitHub repository for format.'''
)
@click.option(
    '-d', '--min-semi-axis',
    type = int,
    help = '''Minimum radius of the cell.'''
)
@click.option(
    '-g', '--max-semi-axis',
    type = int,
    help ='''Maximum radius of the cell.'''
)
@click.option(
    '-r', '--min-area-thresh',
    type = int,
    help = '''Minimum threshold for the cell area.'''
)
@click.option(
    '-m', '--max-area-thresh',
    type = int,
    help = '''Maximum threshold for the cell area.'''
)
@click.option(
    '-a', '--num-chains',
    default = 3000,
    type = int,
    help = '''Number of chains.'''
    '''Default is 3000.'''
)
@click.option(
    '-n', '--num-cluster',
    default = 2,
    type = int,
    help = '''Number of clusters for K-Means Clustering to generate binary image.'''
    '''Default is 2.'''
)
@click.option(
    '-c', '--spatial-distance-pixel-number',
    default = 20,
    type = int,
    help = '''Pixels apart between each grid point to maintain the spatial context.'''
    '''Default is 20.'''
)
@click.option(
    '-s', '--seed',
    default = None,
    type = int,
    help = '''Set random seed so results can be reproduced. By default a random seed is chosen.'''
)
@click.option(
    '-y', '--num_y_pixels_per_block',
    default = 0,
    type = int,
    help = '''Set number of y pixels per block for blocked gibbs. By default, set to 0 implying to let the system decide using greatest common denominator.'''
)
@click.option(
    '-x', '--num_x_pixels_per_block',
    default = 0,
    type = int,
    help = '''Set number of x pixels per block for blocked gibbs. By default, set to 0 implying to let the system decide using greatest common denominator'''
)
@click.option(
    '-p', '--percent',
    default = 0,
    type = int,
    help = '''Top certain percent of blocks of image to analyze'''
)
@click.option(
    '-w', '--gmm_n',
    default = 2,
    type = int,
    help = '''Number of components for Gaussian Mixture Model in Preprocessing'''
)
@click.option(
    '-h', '--log_p_R_option',
    default = "inhomo",
    type = str,
    help = '''Choice of homogeneous or inhomogeneous Prior'''
)
def seg(**kwargs):
    """ Seg the data image using unsupervised Bayesian cell segementation model.
    """
    cellseg.runseg.seg(**kwargs)


@click.command(
    context_settings = {'max_content_width': 120},
    name = 'write-results-file'
)
@click.option(
    '-k', '--in-results_file',
    required = True,
    type = click.Path(exists = True, resolve_path = True),
    help = '''Path to HDF5 format file produced by the `seg` command.'''
)
#@click.option(
#    '-o', '--out-file',
#    required = True,
#    type = click.Path(resolve_path = True),
#    help = '''Path to where results will be written in tsv format.'''
#)
@click.option(
    '-l', '--compress',
    is_flag = True,
    help = '''If set the output file will be compressed using gzip.'''
)
def write_results_file(**kwargs):
    """ Write the results of a fitted model to file.
    """
    objseg.runseg.write_results_file(**kwargs)


@click.group(name='cellseg')
def main():
    pass


main.add_command(seg)
main.add_command(write_results_file)