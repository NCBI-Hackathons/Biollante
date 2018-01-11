# Biollante - detecting modified plant DNA

### Logo, citation, and DOI coming soon

## What is Biollante?

Biollante is a tool for classifying plant DNA as natural or engineered.

## What's the problem?

Genetic engineering is rapidly becoming become commonplace. Increasingly, precise modifications to a genome can be ordered online or performed in a home laboratory.

Given an organism that presents with some new phenotype of interest, we’d like to determine how it came about its novelty - specifically to discern whether it was engineered.

Concerns about proliferation aside, it seems like an interesting scientific question, worth investigating on its own merits: can we identify sequence patterns that are meaningful enough to distinguish between naturally occurring and synthetic DNA?

The possibility of identifying the fingerprints of engineering and other subtle indicators of DNA in the wrong context is an open scientific question. Biollante is our small contribution to this body of research.

## Why not just use BLAST?

This is the first response of many working biologists. And it’s a reasonable question!

If I give you a single sequence - say 1K base pairs - and no other information, it might make sense to just BLAST it against nt and manually interpret the results. “This aligns perfectly with a stretch of Oryza sativa, looks clean to me” or “Half of this is looks like an antiobiotic resistance gene!” Case closed.

But what if I give you hundreds of thousands of sequences, each 10K base pairs. And what about the borderline cases: “Hmm, this looks like T. aestivum on one end, but the other half isn’t showing up. Suspicious...”

Our tool is meant to augment biological expertise, not supplant it. It could be used to suggest regions for greater scrutiny and automatically flag totally normal sequences as safe. A sufficiently powerful model might also be able to recognize deep structural patterns which could evade even an experienced human investigator relying on heuristic manual classifiers.

## What exactly is Biollante?

Biollante is a software repository that aims to predict whether a given DNA sequence is naturally occurring or artificially engineered. We focused on distinguishing natural DNA sequences from model plant organisms from artificially modified plant DNA sequences. Since biological experiments often produce readings of approximately several hundred base pairs at a time, we focused on predictions for base pair sequences of lengths of 500.

To collate a database of natural plant DNA sequences, we started by taking the genomes of eight model plant organisms, and then we took random cuts of size 500 from these genomes. To collate a database of artificial plant DNA sequences, we started by collecting ~150,000 metal resistant genes and ~230 herbicide resistant genes. We then randomly inserted these resistance genes into the plant genomes and took cuts of size 500 again. The parameters for insertion were chosen so that in each artificially engineered plant DNA sequence of 500 base pairs, a subsequence of length between 100 and 300 base pairs was from the resistance gene.

With this data, we built several classifiers based on different methodology.

The first classifier was based on the boosted tree ensemble from the XGBoost library. The featurization we used for this approach was as follows. For each DNA sequence, we labeled each of the 4096 length-6 base pair sequences ("6-mers") with a different number from 1 to 4096. We then converted each DNA sequence into a vector of length 248 by concatenating the labels corresponding to each 6-mers (offsetting consecutive 6-mers by 2 base pairs). We used a training/validation set of 120,000 natural and 120,000 artificial examples, held out 10% of that set for validation, and achieved a validation accuracy of slightly over 70%.

The second classifier was based on the boosted tree ensemble from the XGBoost library, but using a different featurization scheme. Instead of labeling each 6-mer with a different number from 1 to 4096, we labeled 8-mers using a vector embedding which maps an 8-mer to a vector of length 100. We then partitioned each DNA sequence into 8-mers and concatenated the vectors for each 8-mer to compute our representation for each DNA sequence. Using a training/validation set of 20,000 natural and 20,000 artificial example, holding out 10% of that set for validation, we achieved a validation accuracy of 64%.

# How to use <this software>

## Installation options:

We provide two options for installing <this software>: Docker or directly from Github.

### Docker

The Docker image contains <this software> as well as a webserver and FTP server in case you want to deploy the FTP server. It does also contain a web server for testing the <this software> main website (but should only be used for debug purposes).

1. `docker pull ncbihackathons/<this software>` command to pull the image from the DockerHub
2. `docker run ncbihackathons/<this software>` Run the docker image from the master shell script
3. Edit the configuration files as below

### Installing <this software> from Github

1. `git clone https://github.com/NCBI-Hackathons/<this software>.git`
2. Edit the configuration files as below
3. `sh server/<this software>.sh` to test
4. Add cron job as required (to execute <this software>.sh script)

### Configuration

```Examples here```

# Testing

We tested four different tools with <this software>. They can be found in [server/tools/](server/tools/) .

# Additional Functionality

### DockerFile

<this software> comes with a Dockerfile which can be used to build the Docker image.

  1. `git clone https://github.com/NCBI-Hackathons/<this software>.git`
  2. `cd server`
  3. `docker build --rm -t <this software>/<this software> .`
  4. `docker run -t -i <this software>/<this software>`

### Website

There is also a Docker image for hosting the main website. This should only be used for debug purposes.

  1. `git clone https://github.com/NCBI-Hackathons/<this software>.git`
  2. `cd Website`
  3. `docker build --rm -t <this software>/website .`
  4. `docker run -t -i <this software>/website`
