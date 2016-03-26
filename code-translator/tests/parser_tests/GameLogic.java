import java.awt.Graphics2D;
import java.awt.Rectangle;
import java.awt.image.BufferedImage;
import java.util.Random;

public class GameLogic
{
	//Define variables
	private final int asSpeed = 5, spSpeed = 4, shotSpeed = 10, ASTRNUM = 4, MAXFIREBALLS = 100, SPACE = 200, TRANSFORM = 3;
	private int pwidth, pheight, num, life = 3;
	private Random randomGenerator = new Random(); //To generate random location
	private Asteroid currentAstroid1, currentAstroid2 ;
	private boolean spaceShipHitted = false;
	private boolean gameOver = false, win = false;

	//Create game objects
	protected SpaceShip gameSpaceShip;
	private Asteroid[] asteroids;
	private FireBall[] fireballs;

	//Create buffered images
	private BufferedImage bufferdSpaceshipImg = null;
	private BufferedImage bufferedAstroidSmall = null;
	private BufferedImage bufferedAstroidMiddle = null;
	private BufferedImage bufferedAstroidBig = null;

	public GameLogic(int pwidth, int pheight, BufferedImage a, BufferedImage b, BufferedImage c, BufferedImage d)
	{
		this.pwidth = pwidth;
		this.pheight = pheight;
		bufferdSpaceshipImg = a;
		bufferedAstroidSmall = b;
		bufferedAstroidMiddle = c ;
		bufferedAstroidBig = d;
		num = (int) Math.pow(ASTRNUM, TRANSFORM); // Create array in a size of maximum possible asteroids after transform
		//Create game objects
		gameSpaceShip = new SpaceShip((pwidth-bufferdSpaceshipImg.getWidth(null))/2, (pheight-bufferdSpaceshipImg.getHeight(null))/2, pwidth, pheight, bufferdSpaceshipImg, spSpeed, 0);
		fireballs = new FireBall[MAXFIREBALLS];
		createAstroids();

	}

}
