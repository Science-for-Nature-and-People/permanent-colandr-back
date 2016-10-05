package org.datakind.ci.pdfestrian.extraction

import cc.factorie.DenseTensor1
import cc.factorie.app.nlp.{Document, Sentence}

import scala.io.Source

/**
  * Created by sameyeam on 8/3/16.
  */
object Word2VecSent {
  val vectors = Source.fromInputStream(getClass.getResourceAsStream("/glove.6B.300d.txt")).getLines().map { word =>
    val split = word.split(" ")
    split.head -> new DenseTensor1(split.takeRight(300).map{_.toDouble}.toArray)
  }.toMap
  var  i = -1
   val wordCounts = Source.fromInputStream(getClass.getResourceAsStream("/words.sample.doc.counts.old")).getLines().map{ s =>
    val split = s.split(",")
     i += 1
     split.head -> (split.last.toInt, i)
   }.toMap

  val arrayCounts = wordCounts.map{ _._2.swap}.toSeq.sortBy(_._1).map{_._2}
  val words = wordCounts.map{ a => a._2._2 -> a._1}.toSeq.sortBy(_._1).map{_._2}

  val stopWords = Source.fromInputStream(getClass.getResourceAsStream("/stopwords.txt")).getLines().map{ _.toLowerCase}.toSet

  val featureSize = 301

  def clean(string : String) : String = {
    val lower = string.toLowerCase()
    lower.filter(_.isLetterOrDigit)
  }

  val N = 920
  val idf = new DenseTensor1(arrayCounts.map{a => math.log(N.toDouble/a.toDouble)}.toArray)

  def apply(sentence : Sentence, location : Double) : DenseTensor1 = {
    //val counts = new Array[Int](featureSize)
    val tensor = new DenseTensor1(featureSize)
    var wordsInTensor = 0
    for(token <- sentence.tokens) {
      val current = clean(token.string)
      if(current.length > 0 && current.count(_.isLetter) > 0 && !stopWords.contains(current)) {
        if(wordCounts.contains(current) && vectors.contains(current)) {
          val count = wordCounts(current)
          tensor += (vectors(current) * idf(count._2))
          wordsInTensor += 1
        }
      }
    }
    tensor /= wordsInTensor.toDouble
    //tensor *= idf
    tensor /= tensor.twoNorm
    tensor(300) = location
    tensor
  }

  def main(args: Array[String]): Unit = {
    val doc = PDFToDocument(args.head)
    val sentences = doc.get._1.sentences.toArray
    for((sent,i) <- sentences.zipWithIndex) {
      val location = i.toDouble/sentences.length.toDouble
      apply(sent, location)
    }
  }



}