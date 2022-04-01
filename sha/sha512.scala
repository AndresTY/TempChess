import java.security.MessageDigest
import scala.collection.mutable.HashMap
import java.security.SecureRandom
import java.util.Base64
import java.nio.charset.StandardCharsets

case class Person(name: String)

object Roxxy{

  val TOKEN_LENGTH = 10

  var hash_map: HashMap[Person,Array[String]]= new HashMap()

  /*
   *:q
   */

  def coding(passwd:String,n:Int):String =
    n match {
      case _ if n==0 => Encriptions.sha512(passwd)
      case _ if n>0 => Encriptions.sha512(coding(passwd, n-1))
  }

  def validation(name: Person, passwd_hash:String):Boolean={
    
    var temp = hash_map.get(name).get
    if (temp(1) == passwd_hash) true else false
    /*hash_map.foreach{
      case(x,xs) => if (name.name==x.name && xs(0)==passwd_hash) true else false 
    }*/
  }

  def generate_sha512_token(token_prefix:Person) : String ={
    // Encriptions.sha512(token_prefix.toString+"."+System.nanoTime() +"."+ Encriptions.generate_token(TOKEN_LENGTH))
  Encriptions.base64(Encriptions.sha512(token_prefix.toString))+"."+Encriptions.base64(Encriptions.sha512(System.nanoTime().toString)) +"."+Encriptions.base64(Encriptions.sha512( Encriptions.generate_token(TOKEN_LENGTH)))
  }

  def login(name: Person, passwd:String): Boolean = {
    validation(name,passwd)
  }

  def create(name:Person, passwd:String): String = {
    val x = generate_sha512_token(name)
    hash_map = hash_map + (name -> Array(coding(passwd,1000),x))
    x
  }

  def stt():Unit={
    hash_map.foreach{
      case (k,v) => println(k +" => "+ v.foreach(x => println(x)))
    }
  }
}

object Encriptions{
  val secure_random = new SecureRandom()
  val TOKEN_CHARS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz_.-"
  def sha512( passwd : String): String = MessageDigest.getInstance("SHA-512").digest(passwd.getBytes("UTF-8")).map("%02x".format(_)).mkString
  def sha256( passwd : String): String = MessageDigest.getInstance("SHA-256").digest(passwd.getBytes("UTF-8")).map("%02x".format(_)).mkString
  def base64(passwd : String): String = Base64.getEncoder.encodeToString(passwd.getBytes(StandardCharsets.UTF_8))
  def generate_token(token_lenght: Int):String={
    val charlen = TOKEN_CHARS.length()
    def generate_token_accumulator(acc:String, number: Int): String ={
      if(number == 0) acc
      else generate_token_accumulator(acc+TOKEN_CHARS(secure_random.nextInt(charlen)).toString, number-1)
    }
    generate_token_accumulator("",token_lenght)
  }
}

object Main{

  def main(args: Array[String]):Unit={
    var a = Person("Andres")
    var b = Person("Andrea")
    var x =Roxxy.create(a,"pokemon")
    var y = Roxxy.create(b,"Pokemon")
    println(x)
    //println(Roxxy.login(a,x))
    //println(Roxxy.login(a,y))
    //Roxxy.stt()
  }

}

